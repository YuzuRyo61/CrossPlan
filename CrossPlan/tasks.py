from __future__ import absolute_import, unicode_literals
from celery import shared_task
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
    logging.info(pformat(dict(dctOD)))
    res = requests.post(
        targetUrl,
        json=dict(dctOD),
        auth=sign_header(fromUser),
        headers=addDefaultHeader()
    )
    res.raise_for_status()
    return f"Accepted: {res.status_code}"
