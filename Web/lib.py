from bs4 import BeautifulSoup

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    if request.user.is_authenticated:
        context.update({'NewPostForm_': NewPostForm()})
    return render(request, template_name, context=context, content_type=content_type, status=status, using=using)

def panigateQuery(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def scraping(text):
    return BeautifulSoup(text, features="html.parser").get_text()
