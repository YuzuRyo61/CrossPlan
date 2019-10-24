import json
import html2markdown

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseNotAllowed, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from CrossPlan.tasks import NewPost as NewPostTask

from fediverse.models import User as UserModel, Post as PostModel, FediverseUser, Follow as FollowModel
from fediverse.views.renderer.actor.Person import RenderUser
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.response import APResponse

from .forms import LoginForm, NewPostForm, EditProfileForm, Settings_PasswordChangeForm
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

def UserFollowing(request, username):
    targetUser = get_object_or_404(UserModel, username__iexact=username)
    renderObj = {
        "targetUser": targetUser,
        "targetUserFollowing": panigateQuery(request, targetUser.following.all(), settings.USER_PER_PAGE)
    }
    return render_NPForm(request, "profile_following.html", renderObj)

def UserFollower(request, username):
    targetUser = get_object_or_404(UserModel, username__iexact=username)
    renderObj = {
        "targetUser": targetUser,
        "targetUserFollower": panigateQuery(request, targetUser.followers.all(), settings.USER_PER_PAGE)
    }
    return render_NPForm(request, "profile_follower.html", renderObj)

def INDEX(request):
    if request.user.is_authenticated:
        timeline = PostModel.objects.all()[0:20] # pylint: disable=no-member
        return render_NPForm(request, 'index.html', {"timeline": timeline})
    else:
        superusers = UserModel.objects.filter(is_superuser=True) # pylint: disable=no-member
        return render(request, 'landing.html', {"endpoint": settings.CP_ENDPOINT, "superusers": superusers})

def FediUser(request, username, host):
    try:
        targetUser = FediverseUser.objects.get(username__iexact=username, Host__iexact=host) # pylint: disable=no-member
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    
    renderObj = {
        "targetUser": targetUser,
        "targetUserPosts": panigateQuery(request, targetUser.posts.all(), settings.OBJECT_PER_PAGE),
        "isFediverseUser": True
    }
    return render_NPForm(request, "profile.html", renderObj)

@login_required
def newPost(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if NewPostForm(request.POST).is_valid():
        NewPostTask.delay(request.user.username, request.POST)
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
def userState(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    state = request.POST.get("changeState")
    if state == None:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "INVALID_FORM",
            "msg": "changeStateに値がありません"
        }}))
    
    if state == "follow":
        if request.POST.get("target") != None:
            try:
                existFollow = FollowModel.objects.get(fromUser=request.user, target=User.objects.get(username__iexact=request.POST["target"])) # pylint: disable=no-member
                existFollow.delete()
                isNewFollow = False
            except ObjectDoesNotExist:
                newFollow = FollowModel(
                    fromUser=request.user,
                    target=get_object_or_404(User, username__iexact=request.POST["target"])
                )
                isNewFollow = True
        elif request.POST.get("targetFedi") != None:
            try:
                existFollow = FollowModel.objects.get(fromUser=request.user, targetFedi=FediverseUser.objects.get(uuid=request.POST["targetFedi"])) # pylint: disable=no-member
                existFollow.delete()
                isNewFollow = False
            except ObjectDoesNotExist:
                newFollow = FollowModel(
                    fromUser=request.user,
                    targetFedi=get_object_or_404(FediverseUser, uuid=request.POST["targetFedi"])
                )
                isNewFollow = True
        else:
            return HttpResponseBadRequest(json.dumps({"error": {
                "code": "INVALID_FORM",
                "msg": "ターゲットが不明です"
            }}))
        
        if isNewFollow:
            newFollow.save()
        return HttpResponse(status=202)

    return HttpResponse(json.dumps({"error": {
        "code": "NOT_IMPLEMENTED",
        "msg": "実装中"
    }}), content_type="application/json", status=501)

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

@login_required
def settings_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            request.user.display_name = form.cleaned_data["display_name"]
            request.user.description = form.cleaned_data["description"]
            request.user.is_bot = form.cleaned_data["is_bot"]
            request.user.save()
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest()
    else:
        return render_NPForm(request, "settings/profile.html", {"profileForm": 
            EditProfileForm({
                "display_name": request.user.display_name,
                "description": html2markdown.convert(request.user.description),
                "is_bot": request.user.is_bot
            })
        })

class settings_Password(PasswordChangeView):
    form_class = Settings_PasswordChangeForm
    success_url = reverse_lazy('Settings_PasswordDone')
    template_name = "settings/password_change.html"

class settings_PasswordDone(PasswordChangeDoneView):
    template_name = "settings/password_done.html"
