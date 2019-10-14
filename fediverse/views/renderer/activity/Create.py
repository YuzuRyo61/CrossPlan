from django.conf import settings

def RenderCreate(idReverse, actorReverse, obj):
    return {
        "id": f"https://{settings.CP_ENDPOINT}{idReverse}",
        "type": "Create",
        "actor": f"https://{settings.CP_ENDPOINT}{actorReverse}",
        "object": obj
    }
