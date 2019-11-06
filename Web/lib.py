import requests
import logging
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
        for ct in httpCT:
            if ct.startswith("application/activity+json") or ct.startswith("application/ld+json"):
                return True
        return False
    elif request.method == "GET":
        httpAcceptRaw = request.META.get("HTTP_ACCEPT")
        if httpAcceptRaw == None:
            return False
        httpAccept = httpAcceptRaw.split(",")
        for i, has in enumerate(httpAccept):
            httpAccept[i] = has.strip()
        for a in httpAccept:
            if a.startswith("application/activity+json") or a.startswith("application/ld+json"):
                return True
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

def getProfWF(username, host):
    try:
        logging.info(f"fetching profile from webfinger: {username}@{host}")
        resRaw = requests.get(
            f"https://{host}/.well-known/webfinger?resource=acct:{username}@{host}"
        )
        res = resRaw.json()
    except:
        logging.error(f"fetch failed: {username}@{host}")
        return None
    
    if res.get("links") == None:
        logging.error(f"fetch failed (no links): {username}@{host}")
        return None

    for link in res["links"]:
        if link.get("rel") == "self" and link.get("type") == "application/activity+json":
            logging.info(f"fetched profile from webfinger: {link.get('href')}")
            return link.get("href")
    
    logging.error(f"fetch failed (no self rel): {username}@{host}")
    return None
