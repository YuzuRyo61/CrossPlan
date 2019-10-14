from django.conf import settings

def RenderTombstone(idReverse):
    return {
        "type": "Tombstone",
        "id": f"https://{settings.CP_ENDPOINT}{idReverse}"
    }
