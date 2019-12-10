from rest_framework import routers
from .views import UserViewSet, FediverseUserViewSet, PostViewSet

router = routers.DefaultRouter()

router.register('user', UserViewSet)
router.register('fediuser', FediverseUserViewSet)
router.register('post', PostViewSet)
