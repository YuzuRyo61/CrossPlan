from rest_framework import routers
from . import views
router = routers.DefaultRouter()

router.register('user', views.UserViewSet)
router.register('fediuser', views.FediverseUserViewSet)
router.register('post', views.PostViewSet)

urlpatterns = [
    routers.url(r'^me/$', views.myUserViewSet.as_view({'get': 'get'}), name="myUser"),
]

urlpatterns += router.urls
