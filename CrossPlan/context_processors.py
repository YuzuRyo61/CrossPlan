from django.conf import settings

def DEFINE_COMMON_VARIABLE(request):
    return {
        "CP_ENDPOINT": settings.CP_ENDPOINT,
        "CP_VERSION": settings.CP_VERSION
    }
