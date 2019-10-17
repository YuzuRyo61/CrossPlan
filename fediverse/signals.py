from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Post, Like

@receiver(post_save, sender=Post)
def savePostSignal(sender, instance, created, **kwargs):
    print("Post signal")

@receiver(post_save, sender=Like)
def savePostLike(sender, instance, created, **kwargs):
    print("liked")

@receiver(pre_delete, sender=Post)
def preDeletePostSignal(sender, instance, using, **kwargs):
    print("Delete signal (pre)")
