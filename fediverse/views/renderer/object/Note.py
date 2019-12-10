from django.conf import settings
from django.urls import reverse

def RenderNote(uuid, published, fromUser, content, to, cc, replyUrl=None):
    return {
        "id": f"https://{settings.CP_ENDPOINT}{reverse('PostDetail', kwargs={'uuid': str(uuid)})}",
        "type": "Note",
        "published": published,
        "attributedTo": f"https://{settings.CP_ENDPOINT}{reverse('UserShow', kwargs={'username': fromUser})}",
        "inReplyTo": replyUrl if replyUrl != None else None,
        "content": content,
        "to": to,
        "cc": cc,
        "url": f"https://{settings.CP_ENDPOINT}{reverse('PostDetail', kwargs={'uuid': str(uuid)})}"
    }
