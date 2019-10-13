import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseGone
from django.http.response import HttpResponse
from django.conf import settings
from django.utils.xmlutils import SimplerXMLGenerator

from fediverse.models import User as UserModel

import re

def WebFinger_HostMeta(request):
    res = HttpResponse(content_type="application/xml")
    xmlHandle = SimplerXMLGenerator(res, settings.DEFAULT_CHARSET)
    xmlHandle.startDocument()
    xmlHandle.startElement("XRD", {"xmlns": "http://docs.oasis-open.org/ns/xri/xrd-1.0"})
    xmlHandle.addQuickElement("Link", attrs={"rel": "lrdd", "type": "application/xrd+xml", "template": "https://" + settings.CP_ENDPOINT + "/.well-known/webfinger?resource={uri}"})
    xmlHandle.endElement("XRD")
    xmlHandle.endDocument()
    return res

def WebFinger_res(request):
    subject = request.GET.get('resource')
    if subject == None:
        return HttpResponseNotFound()
    elif settings.CP_ENDPOINT != request.get_host():
        return HttpResponseBadRequest()
    else:
        subject_parse = re.search(r"acct:(.+)@(.+)", subject)
        if subject_parse == None:
            return HttpResponseNotFound()
        userInfo = get_object_or_404(UserModel, username__iexact=subject_parse.group(1))
        return HttpResponse(json.dumps({
            "subject": "acct:" + userInfo.username + "@" + subject_parse.group(2),
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": "https://" + settings.CP_ENDPOINT + "/user/" + userInfo.username
                },
                {
                    "rel": "http://webfinger.net/rel/profile-page",
                    "type": "text/html",
                    "href": "https://" + settings.CP_ENDPOINT + "/user/" + userInfo.username
                }
            ]
        }, ensure_ascii=False),
        content_type="application/jrd+json; charset=UTF-8"
        )
