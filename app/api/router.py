from rest_framework.routers import DefaultRouter
from .viewsets import *

router = DefaultRouter()
router.register('user_belong_home', user_belong_homeViewSet)
router.register('home_list',home_listViewSet)
router.register('added_device_list', added_device_listViewSet)
router.register('device_type', device_typeViewSet)
router.register('alive_verification_code',
                alive_verification_codeViewSet)
router.register('category', categoryViewSet)
router.register('device_data', device_dataViewSet)
app_name = 'api'