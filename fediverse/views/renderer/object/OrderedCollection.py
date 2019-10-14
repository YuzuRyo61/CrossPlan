from django.conf import settings

def RenderOrderedCollection(idReverse, totalItems, firstReverse, lastReverse=None):
    res = {
        "id": f"https://{settings.CP_ENDPOINT}{idReverse}",
        "type": "OrderedCollection",
        "totalItems": int(totalItems),
        "first": f"https://{settings.CP_ENDPOINT}{firstReverse}"
    }
    if lastReverse != None:
        res["last"] = f"https://{settings.CP_ENDPOINT}{lastReverse}"
    
    return res
