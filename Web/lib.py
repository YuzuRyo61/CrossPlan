def isAPHeader(request):
    if request.method == "POST":
        return True
    elif request.method == "GET":
        httpAcceptRaw = request.META.get("HTTP_ACCEPT")
        print(f"Accept: {httpAcceptRaw}")
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
