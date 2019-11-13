from __future__ import absolute_import, unicode_literals
from celery import shared_task
from collections import OrderedDict
import requests
import markdown
import logging

from django.core.exceptions import ObjectDoesNotExist

from pprint import pformat

from fediverse.models import Post, User
from fediverse.lib import sign_header, addDefaultHeader

# resource: https://dot-blog.jp/news/django-async-celery-redis-mac/
@shared_task(max_retries=10, default_retry_delays=60)
def APSend(targetUrl, fromUser, dct):
    dctOD = OrderedDict(**dct)
    dctOD['@context'] = [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1"
    ]
    dctOD.move_to_end('@context', False)
    logging.info(f"APSEND => {targetUrl}")
    logging.info("APBODY: ")
    logging.info(pformat(dict(dctOD)))
    try:
        res = requests.post(
            targetUrl,
            json=dict(dctOD),
            auth=sign_header(fromUser),
            headers=addDefaultHeader()
        )
        res.raise_for_status()
    except:
        logging.warn("APSend was failed. It will be try to retry.")
        raise APSend.retry()
    return res.status_code

@shared_task
def AccountDeletion(username):
    try:
        target = User.objects.get(username__iexact=username)
    except ObjectDoesNotExist:
        logging.error("Targetted username is not found.")
        raise ValueError("Targetted username is not found.")

    for post in target.posts.all():
        logging.info(f"Delete post: {str(post.uuid)}")
        post.delete()
    
    for following in target.following.all():
        logging.info(f"Delete following: {str(following.uuid)}")
        following.delete()
    
    for followers in target.followers.all():
        logging.info(f"Delete follower: {str(followers.uuid)}")
        followers.delete()
    
    for liked in target.liked.all():
        logging.info(f"Delete liked: {str(liked.uuid)}")
        liked.delete()

    for blocking in target.blocking.all():
        logging.info(f"Delete blocking: {str(blocking.uuid)}")
        blocking.delete()

    for blocked in target.blocked.all():
        logging.info(f"Deleteblocked: {str(blocked.uuid)}")
        blocked.delete()
    
    return True
