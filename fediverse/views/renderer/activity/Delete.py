from django.conf import settings

def RenderDelete(actorReverse, obj):
    return {
        "type": "Delete",
        "actor": f"https://{settings.CP_ENDPOINT}{actorReverse}",
        "object": obj
    }
