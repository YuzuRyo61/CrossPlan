from django.conf import settings
from django.urls import reverse

def RenderTombstone(uuid):
    return {
        "type": "Tombstone",
        "id": f"https://{settings.CP_ENDPOINT}{reverse('PostDetail', kwargs={'uuid': str(uuid)})}"
    }
