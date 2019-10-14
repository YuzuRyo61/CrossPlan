from django.conf import settings

def RenderNote(idReverse, published, attrReverse, content, to, cc, url, replyReverse=None):
    return {
        "id": f"https://{settings.CP_ENDPOINT}{idReverse}",
        "type": "Note",
        "published": published,
        "attributedTo": f"https://{settings.CP_ENDPOINT}{attrReverse}",
        "inReplyTo": f"https://{settings.CP_ENDPOINT}{replyReverse}" if replyReverse != None else None,
        "content": content,
        "to": to,
        "cc": cc,
        "url": url
    }
