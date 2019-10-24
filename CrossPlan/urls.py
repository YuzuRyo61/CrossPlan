"""CrossPlan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Web import views as WebViews
from fediverse.views.WebFinger import WebFinger_HostMeta, WebFinger_res

urlpatterns = [
    path('', WebViews.INDEX, name="INDEX"),
    path('ACP/', admin.site.urls),
    path('.well-known/hostmeta', WebFinger_HostMeta),
    path('.well-known/webfinger', WebFinger_res),
    path('AP/', include('fediverse.urls')),
    path('user/<username>', WebViews.User, name="UserShow"),
    path('user/<username>/following', WebViews.UserFollowing, name="UserShowFollowing"),
    path('user/<username>/follower', WebViews.UserFollower, name="UserShowFollower"),
    path('login', WebViews.LoginView.as_view(), name="Login"),
    path('logout', WebViews.LogoutView.as_view(), name="Logout"),
    path('_NEWPOST', WebViews.newPost, name="NewPost"),
    path('_ANNOUNCE', WebViews.announce, name="Announce"),
    path('_FAVORITE', WebViews.favorite, name="Favorite"),
    path('_DELETEPOST', WebViews.postDelete, name="DeletePost"),
    path('_USERSTATE', WebViews.userState, name="UserState"),
    path('post/<uuid>', WebViews.postDetail, name="PostDetail"),
    path('settings/profile', WebViews.settings_profile, name="Settings_Profile"),
    path('settings/password', WebViews.settings_Password.as_view(), name="Settings_Password"),
    path('settings/password/done', WebViews.settings_PasswordDone.as_view(), name="Settings_PasswordDone"),    
    path('fediuser/<username>@<host>', WebViews.FediUser, name="FediUserShow")
]
