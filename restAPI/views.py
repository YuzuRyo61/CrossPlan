from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from fediverse.models import User, FediverseUser, Post

from .serializer import UserModelSerializer, FediverseUserModelSerializer, PostModelSerializer

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all() # pylint: disable=no-member
    serializer_class = UserModelSerializer

class FediverseUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FediverseUser.objects.all() # pylint: disable=no-member
    serializer_class = FediverseUserModelSerializer

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all() # pylint: disable=no-member
    serializer_class = PostModelSerializer

class myUserViewSet(viewsets.ViewSet):
    """
    自分のユーザーを表示します。
    ※認証が必要（OAuthもしくはセッション）
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all() # pylint: disable=no-member

    def get(self, request):
        serializer = UserModelSerializer(get_object_or_404(self.queryset, username=request.user.username))
        return Response(serializer.data)
