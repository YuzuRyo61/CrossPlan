from rest_framework import serializers

from fediverse.models import User, FediverseUser, Post

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'display_name', 'description', 'is_bot', 'is_manualFollow', 'is_staff', 'is_superuser', 'is_suspended', 'registered', 'updated')

class FediverseUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FediverseUser
        fields = ('uuid', 'username', 'Host', 'display_name', 'description', 'is_bot', 'is_manualFollow', 'Url')

class PostModelSerializer(serializers.ModelSerializer):
    parent = UserModelSerializer(many=False, read_only=True)
    parentFedi = FediverseUserModelSerializer(many=False, read_only=True)
    announceTo = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    replyTo = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('uuid', 'body', 'parent', 'parentFedi', 'announceTo', 'replyTo', 'posted')
