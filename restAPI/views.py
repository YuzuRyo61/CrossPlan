from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

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
