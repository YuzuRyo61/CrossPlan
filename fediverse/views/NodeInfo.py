import json

from django.urls import reverse
from django.conf import settings
from django.http.response import HttpResponse

from fediverse.models import User

def NodeInfo_wk(request):
    return HttpResponse(json.dumps({"links": [
        {
            "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
            "href": f"https://{settings.CP_ENDPOINT}{reverse('NodeInfo')}"
        }
    ]}), content_type="application/json")

def NodeInfo(request):
    return HttpResponse(json.dumps({
        "version": "2.0",
        "software": {
            "name": "crossplan",
            "version": str(settings.CP_VERSION)
        },
        "protocols": ["activitypub"],
        "services": {
            "inbound": [],
            "outbound": []
        },
        "openRegistrations": False,
        "usage": {
            "users": {
                "total": User.objects.filter(is_active=True).count(),
                "activeHalfyear": 0,
                "activeMonth": 0
            }
        },
        "metadata": {

        }
    }), content_type="application/json")
