from __future__ import absolute_import, unicode_literals
from celery import shared_task
from urllib.parse import urlparse
from collections import OrderedDict
import requests
import markdown
import logging

from pprint import pformat

from fediverse.models import Post, User
from fediverse.lib import sign_header, addDefaultHeader

# resource: https://dot-blog.jp/news/django-async-celery-redis-mac/
@shared_task
def APSend(targetUrl, fromUser, dct):
    dctOD = OrderedDict(**dct)
    dctOD['@context'] = [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1"
    ]
    dctOD.move_to_end('@context', False)
    logging.info(f"APSEND => {targetUrl}")
    logging.info("APBODY: ")
    logging.info(pformat(dct))
    res = requests.post(
        targetUrl,
        json=dct,
        auth=sign_header(fromUser),
        headers=addDefaultHeader()
    )
    res.raise_for_status()
    return f"Accepted: {res.status_code}"

@shared_task
def NewPost(fromUser, post_content):
    targetUser = User.objects.get(username__iexact=fromUser)
    newPost = Post(
        body=markdown.Markdown().convert(post_content['body']),
        parent=targetUser
    )
    newPost.save()
    return newPost
