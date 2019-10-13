import json

from django.http.response import HttpResponse

def APResponse(dct):
    return HttpResponse(
        content=json.dumps(dct, ensure_ascii=False),
        content_type="application/activity+json"
    )
