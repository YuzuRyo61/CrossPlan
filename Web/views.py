from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from fediverse.models import User as UserModel
from fediverse.views.renderer.actor.Person import RenderUser
from fediverse.views.renderer.head import APRender
from fediverse.views.renderer.response import APResponse

from .forms import LoginForm
from .lib import isAPHeader

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
        return render(request, "profile.html", {"targetUser": targetUser})

@login_required
def INDEX(request):
    return render(request, 'index.html')
