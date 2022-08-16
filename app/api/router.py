from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet
from .viewsets import *

router = DefaultRouter()
# router.register('user_belong_home', user_homeViewSet)
router.register('home_list',homeViewSet)
router.register("home_admin", homeAdminViewSet)
router.register('added_device_list', added_device_listViewSet)
router.register('device_type', device_typeViewSet)
router.register('category', categoryViewSet)
router.register('device_data', device_dataViewSet)
router.register('mode_key_data', mode_key_dataViewSet)
router.register('user', UserViewSet)
app_name = 'api'