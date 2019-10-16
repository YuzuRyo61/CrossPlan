from django.shortcuts import render

from Web.forms import NewPostForm

def isAPHeader(request):
    if request.method == "POST":
        httpCTRaw = request.META.get("CONTENT_TYPE")
        if httpCTRaw == None:
            return False
        httpCT = httpCTRaw.split(",")
        for i, has in enumerate(httpCT):
            httpCT[i] = has.strip()
        if "application/activity+json" in httpCT or "application/ld+json" in httpCT:
            return True
        else:
            return False
    elif request.method == "GET":
        httpAcceptRaw = request.META.get("HTTP_ACCEPT")
        if httpAcceptRaw == None:
            return False
        httpAccept = httpAcceptRaw.split(",")
        for i, has in enumerate(httpAccept):
            httpAccept[i] = has.strip()
        if "application/activity+json" in httpAccept or "application/ld+json" in httpAccept:
            return True
        else:
            return False
    else:
        return None

def render_NPForm(request, template_name, context={}, content_type=None, status=None, using=None):
    context.update({'NewPostForm_': NewPostForm()})
    return render(request, template_name, context=context, content_type=content_type, status=status, using=using)
