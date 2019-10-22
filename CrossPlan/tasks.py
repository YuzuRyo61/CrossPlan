from __future__ import absolute_import, unicode_literals
from celery import shared_task
from urllib.parse import urlparse
import requests
import markdown

from fediverse.models import Post, User
from fediverse.lib import sign_header, addDefaultHeader

# resource: https://dot-blog.jp/news/django-async-celery-redis-mac/
@shared_task
def APSend(targetUrl, fromUser, dct):
    requests.post(
        targetUrl,
        json=dct,
        auth=sign_header(fromUser),
        headers=addDefaultHeader()
    ).raise_for_status()
    return True

@shared_task
def NewPost(fromUser, post_content):
    targetUser = User.objects.get(username__iexact=fromUser)
    newPost = Post(
        body=markdown.Markdown().convert(post_content['body']),
        parent=targetUser
    )
    newPost.save()
    return newPost
