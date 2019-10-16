from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from CrossPlan.tasks import NewPost as NewPostTask

from fediverse.models import User as UserModel
from fediverse.views.renderer.actor.Person import RenderUser
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.response import APResponse

from .forms import LoginForm
from .lib import isAPHeader, render_NPForm, panigateQuery

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
        if request.user.is_authenticated:
            return render_NPForm(request, renderTarget, renderObj)
        else:
            return render(request, renderTarget, renderObj)

@login_required
def INDEX(request):
    return render_NPForm(request, 'index.html')

@login_required
def newPost(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    NewPostTask(request.user.username, request.POST)

    return HttpResponse(status=204)
