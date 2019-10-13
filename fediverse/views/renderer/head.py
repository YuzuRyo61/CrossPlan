from collections import OrderedDict

def APRender(obj):
    res = OrderedDict(**obj)
    res['@context'] = [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1"
    ]
    res.move_to_end('@context', False)
    return dict(res)
