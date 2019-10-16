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
    path('login', WebViews.LoginView.as_view(), name="Login"),
    path('logout', WebViews.LogoutView.as_view(), name="Logout"),
    path('_NEWPOST', WebViews.newPost, name="NewPost")
]
