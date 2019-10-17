import json

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseNotAllowed, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from CrossPlan.tasks import NewPost as NewPostTask

from fediverse.models import User as UserModel, Post as PostModel
from fediverse.views.renderer.actor.Person import RenderUser
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.response import APResponse

from .forms import LoginForm, NewPostForm
from .lib import isAPHeader, render_NPForm, panigateQuery, scraping

# Create your views here.
class LoginView(LoginView): # pylint: disable=function-redefined
    form_class = LoginForm
    template_name = "login.html"

class LogoutView(LoginRequiredMixin, LogoutView): # pylint: disable=function-redefined
    template_name = "logout.html"

def User(request, username):
    if isAPHeader(request):
        return APResponse(APRender(RenderUser(username)))
    else:
        targetUser = get_object_or_404(UserModel, username__iexact=username)
        renderObj = {
            "targetUser": targetUser,
            "targetUserPosts": panigateQuery(request, targetUser.posts.all(), settings.OBJECT_PER_PAGE)
        }
        renderTarget = "profile.html"
        return render_NPForm(request, renderTarget, renderObj)

def INDEX(request):
    if request.user.is_authenticated:
        return render_NPForm(request, 'index.html')
    else:
        superusers = UserModel.objects.filter(is_superuser=True) # pylint: disable=no-member
        return render(request, 'landing.html', {"endpoint": settings.CP_ENDPOINT, "superusers": superusers})

@login_required
def newPost(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if NewPostForm(request.POST).is_valid():
        NewPostTask(request.user.username, request.POST)
    else:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "DO_NOT_EMPTY",
            "msg": "空の投稿は投稿できません。"
        }}), content_type="application/json")

    return HttpResponse(status=204)

@login_required
def announce(request):
    pass

@login_required
def favorite(request):
    pass

@login_required
def postDelete(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")
    target = get_object_or_404(PostModel, uuid=request.POST.get('uuid'))
    if request.user == target.parent:
        target.delete()
        return HttpResponseRedirect(reverse("INDEX"))
    else:
        return HttpResponseForbidden()

def postDetail(request, uuid):
    post = get_object_or_404(PostModel, uuid=uuid)
    return render_NPForm(request, "postDetail.html", {"post": post, "scraped_body": scraping(post.body)})
