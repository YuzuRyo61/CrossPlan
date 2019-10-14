from __future__ import absolute_import, unicode_literals
from celery import shared_task
from urllib.parse import urlparse
import requests

from fediverse.lib import sign_header

# resource: https://dot-blog.jp/news/django-async-celery-redis-mac/

@shared_task
def APSend(targetUrl, fromUser, dct):
    requests.post(
        targetUrl,
        json=dct,
        headers=sign_header(fromUser, "POST", urlparse(targetUrl).path)
    ).raise_for_status()
    return True
