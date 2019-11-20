import json
import html2markdown

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponseNotAllowed, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, HttpResponseGone, Http404, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.views.generic import CreateView

from CrossPlan.tasks import AccountDeletion

from fediverse.models import User as UserModel, Post as PostModel, FediverseUser, Follow as FollowModel, Like as LikeModel
from fediverse.lib import registerFediUser
from fediverse.views.renderer.actor.Person import RenderUser
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.response import APResponse

from .forms import LoginForm, NewPostForm, EditProfileForm, Settings_PasswordChangeForm, EditPrivacyForm, RegisterForm, convertMarkdown
from .lib import isAPHeader, render_NPForm, panigateQuery, scraping, getProfWF

# Create your views here.
class RegisterView(CreateView):
    def post(self, request, *args, **kwargs):
        if not settings.CP_OPENREGISTER:
            return HttpResponseForbidden()
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("/")
        else:
            return render_NPForm(request, "register.html", {"form": form})
        
    def get(self, request, *args, **kwargs):
        if not settings.CP_OPENREGISTER:
            return HttpResponseForbidden()
        form = RegisterForm()
        return render_NPForm(request, "register.html", {"form": form})

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
        if targetUser.is_active == False:
            return HttpResponseGone()
        renderObj = {
            "targetUser": targetUser,
            "targetUserPosts": panigateQuery(request, targetUser.posts.all(), settings.OBJECT_PER_PAGE),
            "targetUserCount": {
                "following": targetUser.following.filter(is_pending=False).count(),
                "followers": targetUser.followers.filter(is_pending=False).count()
            }
        }
        if request.user.is_authenticated and request.user != targetUser:
            renderObj.update({
                "targetUserRelation": {
                    "following": True if targetUser.followers.filter(fromUser=request.user, is_pending=False).count() else False,
                    "followed": True if targetUser.following.filter(target=request.user, is_pending=False).count() else False,
                    "followPending": True if targetUser.followers.filter(fromUser=request.user, is_pending=True).count() else False,
                    "blocked": True if targetUser.blocking.filter(target=request.user).count() else False,
                }
            })
        return render_NPForm(request, "profile.html", renderObj)

def UserFollowing(request, username):
    targetUser = get_object_or_404(UserModel, username__iexact=username)
    if targetUser.is_active == False:
        return HttpResponseGone()
    renderObj = {
        "targetUser": targetUser,
        "targetUserFollowing": panigateQuery(request, targetUser.following.filter(is_pending=False), settings.USER_PER_PAGE),
        "targetUserCount": {
            "following": targetUser.following.filter(is_pending=False).count(),
            "followers": targetUser.followers.filter(is_pending=False).count()
        }
    }
    if request.user.is_authenticated and request.user != targetUser:
        renderObj.update({
            "targetUserRelation": {
                "following": True if targetUser.followers.filter(fromUser=request.user, is_pending=False).count() else False,
                "followed": True if targetUser.following.filter(target=request.user, is_pending=False).count() else False,
                "followPending": True if targetUser.followers.filter(fromUser=request.user, is_pending=True).count() else False,
                "blocked": True if targetUser.blocking.filter(target=request.user).count() else False,
            }
        })
    return render_NPForm(request, "profile_following.html", renderObj)

def UserFollower(request, username):
    targetUser = get_object_or_404(UserModel, username__iexact=username)
    if targetUser.is_active == False:
        return HttpResponseGone()
    renderObj = {
        "targetUser": targetUser,
        "targetUserFollower": panigateQuery(request, targetUser.followers.filter(is_pending=False), settings.USER_PER_PAGE),
        "targetUserCount": {
            "following": targetUser.following.filter(is_pending=False).count(),
            "followers": targetUser.followers.filter(is_pending=False).count()
        }
    }
    if request.user.is_authenticated and request.user != targetUser:
        renderObj.update({
            "targetUserRelation": {
                "following": True if targetUser.followers.filter(fromUser=request.user, is_pending=False).count() else False,
                "followed": True if targetUser.following.filter(target=request.user, is_pending=False).count() else False,
                "followPending": True if targetUser.followers.filter(fromUser=request.user, is_pending=True).count() else False,
                "blocked": True if targetUser.blocking.filter(target=request.user).count() else False,
            }
        })
    return render_NPForm(request, "profile_follower.html", renderObj)

def INDEX(request):
    if request.user.is_authenticated:
        timeline = PostModel.objects.all()[0:20] # pylint: disable=no-member
        return render_NPForm(request, 'index.html', {"timeline": timeline})
    else:
        superusers = UserModel.objects.filter(is_superuser=True) # pylint: disable=no-member
        return render(request, 'landing.html', {"superusers": superusers})

def FediUser(request, username, host):
    try:
        targetUser = FediverseUser.objects.get(username__iexact=username, Host__iexact=host) # pylint: disable=no-member
    except ObjectDoesNotExist:
        targetUrl = getProfWF(username, host)
        if targetUrl == None:
            raise Http404()
        targetUser = registerFediUser(targetUrl)
        if targetUser == None:
            return HttpResponse(status=500)
        targetUser.save()
    
    renderObj = {
        "targetUser": targetUser,
        "targetUserPosts": panigateQuery(request, targetUser.posts.all(), settings.OBJECT_PER_PAGE),
        "isFediverseUser": True,
        "targetUserCount": {
            "following": targetUser.following.filter(is_pending=False).count(),
            "followers": targetUser.followers.filter(is_pending=False).count()
        }
    }
    if request.user.is_authenticated:
        renderObj.update({
            "targetUserRelation": {
                "following": True if targetUser.followers.filter(fromUser=request.user, is_pending=False).count() else False,
                "followed": True if targetUser.following.filter(target=request.user, is_pending=False).count() else False,
                "followPending": True if targetUser.followers.filter(fromUser=request.user, is_pending=True).count() else False,
                "blocked": True if targetUser.blocking.filter(target=request.user).count() else False,
            }
        })
    return render_NPForm(request, "profile.html", renderObj)

def FediUserFollowing(request, username, host):
    try:
        targetUser = FediverseUser.objects.get(username__iexact=username, Host__iexact=host) # pylint: disable=no-member
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    
    renderObj = {
        "targetUser": targetUser,
        "targetUserFollowing": panigateQuery(request, targetUser.following.filter(is_pending=False), settings.USER_PER_PAGE),
        "isFediverseUser": True,
        "targetUserCount": {
            "following": targetUser.following.filter(is_pending=False).count(),
            "followers": targetUser.followers.filter(is_pending=False).count()
        }
    }
    if request.user.is_authenticated:
        renderObj.update({
            "targetUserRelation": {
                "following": True if targetUser.followers.filter(fromUser=request.user, is_pending=False).count() else False,
                "followed": True if targetUser.following.filter(target=request.user, is_pending=False).count() else False,
                "followPending": True if targetUser.followers.filter(fromUser=request.user, is_pending=True).count() else False,
                "blocked": True if targetUser.blocking.filter(target=request.user).count() else False,
            }
        })
    return render_NPForm(request, "profile_following.html", renderObj)

def FediUserFollower(request, username, host):
    try:
        targetUser = FediverseUser.objects.get(username__iexact=username, Host__iexact=host) # pylint: disable=no-member
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    
    renderObj = {
        "targetUser": targetUser,
        "targetUserFollower": panigateQuery(request, targetUser.followers.filter(is_pending=False), settings.USER_PER_PAGE),
        "isFediverseUser": True,
        "targetUserCount": {
            "following": targetUser.following.filter(is_pending=False).count(),
            "followers": targetUser.followers.filter(is_pending=False).count()
        }
    }
    if request.user.is_authenticated:
        renderObj.update({
            "targetUserRelation": {
                "following": True if targetUser.followers.filter(fromUser=request.user, is_pending=False).count() else False,
                "followed": True if targetUser.following.filter(target=request.user, is_pending=False).count() else False,
                "followPending": True if targetUser.followers.filter(fromUser=request.user, is_pending=True).count() else False,
                "blocked": True if targetUser.blocking.filter(target=request.user).count() else False,
            }
        })
    return render_NPForm(request, "profile_follower.html", renderObj)

@login_required
def newPost(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if NewPostForm(request.POST).is_valid():
        newPostObj = PostModel(
            parent=request.user,
            body=convertMarkdown(request.POST["body"])
        )
        newPostObj.save()
        return HttpResponse(status=204)
    else:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "DO_NOT_EMPTY",
            "msg": "空の投稿は投稿できません。"
        }}), content_type="application/json")

@login_required
def announce(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if request.POST.get("target", None) == None:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "INVALID_FORM",
            "msg": "対象の投稿が不明です。"
        }}), content_type="application/json")
    
    try:
        obj = PostModel.objects.get(uuid=request.POST.get("target", None)) # pylint: disable=no-member
    except ObjectDoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "POST_NOTFOUND",
            "msg": "対象の投稿が見つかりません。"
        }}), content_type="application/json")

    newAnnounce = PostModel(
        parent=request.user,
        announceTo=obj
    )
    newAnnounce.save()

    return HttpResponse(status=204)

@login_required
def favorite(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if request.POST.get("target", None) == None:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "INVALID_FORM",
            "msg": "対象の投稿が不明です。"
        }}), content_type="application/json")

    try:
        obj = PostModel.objects.get(uuid=request.POST.get("target", None)) # pylint: disable=no-member
    except ObjectDoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "POST_NOTFOUND",
            "msg": "対象の投稿が見つかりません。"
        }}), content_type="application/json")

    try:
        isExist = LikeModel.objects.get(target=obj, fromUser=request.user) # pylint: disable=no-member
        isExist.delete()
        Liked = False
    except ObjectDoesNotExist:
        newLike = LikeModel(target=obj, fromUser=request.user)
        newLike.save()
        Liked = True

    return JsonResponse({"liked": Liked, "target": request.POST.get("target", None)})

@login_required
def likedPosts(request):
    return render_NPForm(request, "likedPosts.html", {
        "likedPosts": panigateQuery(request, [obj.target for obj in request.user.liked.all().order_by('created').reverse()], settings.OBJECT_PER_PAGE)
    })

def userState(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if not request.user.is_authenticated:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "NOT_AUTHENTICATED",
            "msg": "ログインが必要です。"
        }}))

    state = request.POST.get("changeState")
    if state == None:
        return HttpResponseBadRequest(json.dumps({"error": {
            "code": "INVALID_FORM",
            "msg": "changeStateに値がありません"
        }}))

    if state == "follow":
        if request.POST.get("target") != None:
            try:
                existFollow = FollowModel.objects.get(fromUser=request.user, target=UserModel.objects.get(username__iexact=request.POST["target"])) # pylint: disable=no-member
                existFollow.delete()
                isNewFollow = False
            except ObjectDoesNotExist:
                newFollow = FollowModel(
                    fromUser=request.user,
                    target=get_object_or_404(UserModel, username__iexact=request.POST["target"])
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
        return HttpResponse(status=204)

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
    if post.parent != None and post.parent.is_active == False:
        return HttpResponseGone()
    obj = {"post": post}
    if post.announceTo == None:
        obj.update({"scraped_body": scraping(post.body)})
    else:
        obj.update({"scraped_body": f"AN: {scraping(post.announceTo.body)}"})
    return render_NPForm(request, "postDetail.html", obj)

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

@login_required
def settings_deleteAccount(request):
    return render_NPForm(request, "settings/delete_account.html")

@login_required
def settings_deleteAccountDone(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")
    
    if not request.user.is_superuser:
        request.user.is_active = False
        request.user.save()
        AccountDeletion.delay(request.user.username)
        logout(request)
        return render_NPForm(request, "settings/delete_account_done.html")
    else:
        return HttpResponseForbidden()

def settings_privacy(request):
    if request.method == "POST":
        form = EditPrivacyForm(request.POST)
        if form.is_valid():
            request.user.is_manualFollow = form.cleaned_data["is_manualFollow"]
            request.user.save()
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest()
    else:
        return render_NPForm(request, "settings/privacy.html", {"profileForm": 
            EditPrivacyForm({
                "is_manualFollow": request.user.is_manualFollow
            })
        })
