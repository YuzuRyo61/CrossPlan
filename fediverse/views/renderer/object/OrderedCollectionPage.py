from django.conf import settings

def RenderOrderedCollectionPage(idReverse, partOfReverse, totalItems, orderedItems, nextReverse=None, prevReverse=None):
    res = {
        "id": f"https://{settings.CP_ENDPOINT}{idReverse}",
        "type": "OrderedCollectionPage",
        "totalItems": int(totalItems)
    }
    if nextReverse != None:
        res["next"] = f"https://{settings.CP_ENDPOINT}{nextReverse}"
    
    if prevReverse != None:
        res["prev"] = f"https://{settings.CP_ENDPOINT}{prevReverse}"

    res["partOf"] = f"https://{settings.CP_ENDPOINT}{partOfReverse}"
    res["orderedItems"] = orderedItems

    return res
