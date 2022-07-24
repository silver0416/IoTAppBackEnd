from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('user_info', views.user_infoViewSet)
router.register('user_belong_home', views.user_belong_homeViewSet)
router.register('home_list', views.home_listViewSet)
router.register('added_device_list', views.added_device_listViewSet)
router.register('device_type', views.device_typeViewSet)
router.register('alive_verification_code', views.alive_verification_codeViewSet)
router.register('category', views.categoryViewSet)
router.register('device_data', views.device_dataViewSet)
app_name = 'api'

urlpatterns = [
    path('', include(router.urls) ),
]