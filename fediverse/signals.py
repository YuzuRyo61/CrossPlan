import logging
from urllib.parse import urlparse

from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from CrossPlan.tasks import APSend

from .models import Post, Like, Follow
from .views.renderer.head import APRender
from .views.renderer.activity.Create import RenderCreate
from .views.renderer.activity.Delete import RenderDelete
from .views.renderer.activity.Follow import RenderFollow
from .views.renderer.activity.Undo import RenderUndo
from .views.renderer.object.Note import RenderNote
from .views.renderer.object.Tombstone import RenderTombstone

from pprint import pprint as pp

@receiver(post_save, sender=Post)
def savePostSignal(sender, instance, created, **kwargs):
    if created and instance.parent != None:
        logging.info(f"SEND [CREATE] => {str(instance.uuid)}")
        sent_domains = []
        for followers in instance.parent.followers.all():
            if followers.fromFediUser != None:
                if followers.fromFediUser.Host in sent_domains:
                    continue
                APSend.delay(
                    followers.fromFediUser.SharedInbox if followers.fromFediUser.SharedInbox != None else followers.fromFediUser.Inbox,
                    instance.parent.username,
                    APRender(RenderCreate(
                        instance.uuid,
                        instance.parent.username,
                        RenderNote(
                            instance.uuid,
                            instance.posted.isoformat(),
                            instance.parent.username,
                            instance.body,
                            ["https://www.w3.org/ns/activitystreams#Public"],
                            [f"https://{settings.CP_ENDPOINT}{reverse('Fediverse:Followers', kwargs={'username': instance.parent.username})}"]
                        )
                    ))
                )
                sent_domains.append(followers.fromFediUser.Host)

@receiver(post_save, sender=Like)
def savePostLike(sender, instance, created, **kwargs):
    print("liked")

@receiver(pre_delete, sender=Post)
def preDeletePostSignal(sender, instance, using, **kwargs):
    if instance.parent != None:
        print(f"SEND [DELETE] => {str(instance.uuid)}")
        for followers in instance.parent.followers.all():
            if followers.fromFediUser != None:
                APSend.delay(
                    followers.fromFediUser.SharedInbox if followers.fromFediUser.SharedInbox != None else followers.fromFediUser.Inbox,
                    instance.parent.username,
                    APRender(RenderDelete(
                        instance.parent.username,
                        RenderTombstone(instance.uuid)
                    ))
                )

@receiver(post_save, sender=Follow)
def postFollow(sender, instance, created, **kwargs):
    if created and instance.targetFedi != None and instance.fromUser != None:
        APSend.delay(
            instance.targetFedi.Inbox,
            instance.fromUser.username,
            APRender(RenderFollow(
                instance.fromUser.username,
                instance.uuid,
                f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': instance.fromUser.username})}",
                instance.targetFedi.Uri
            ))
        )

@receiver(pre_delete, sender=Follow)
def preUnFollow(sender, instance, using, **kwargs):
    if instance.targetFedi != None:
        APSend.delay(
            instance.targetFedi.Inbox,
            instance.fromUser.username,
            APRender(RenderUndo(
                instance.fromUser.username,
                RenderFollow(
                    instance.fromUser.username,
                    instance.uuid,
                    f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': instance.fromUser.username})}",
                    instance.targetFedi.Uri
                )
            ))
        )
