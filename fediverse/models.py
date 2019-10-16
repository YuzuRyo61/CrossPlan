import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from fediverse.lib import generate_key

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            username=username
        )
        user.set_password(password)
        kp = generate_key()
        user.privateKey = kp[0]
        user.publicKey = kp[1]
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        primary_key=True,
        max_length=16,
        unique=True
    )
    display_name = models.CharField(
        max_length=32,
        blank=True,
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_bot = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_silence = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    registered = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publicKey = models.TextField(blank=True, editable=False)
    privateKey = models.TextField(blank=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"@{self.username}"

class FediverseUser(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=64)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    Host = models.URLField()
    Inbox = models.URLField(blank=True, null=True)
    Outbox = models.URLField(blank=True, null=True)
    SharedInbox = models.URLField(blank=True, null=True)
    Featured = models.URLField(blank=True, null=True)
    Followers = models.URLField(blank=True, null=True)
    Following = models.URLField(blank=True, null=True)
    Uri = models.URLField(blank=True, null=True)
    Url = models.URLField(blank=True, null=True)
    publicKey = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"@{self.username}@{self.Host}"

class Post(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    parentFedi = models.ForeignKey(FediverseUser, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-posted', )
