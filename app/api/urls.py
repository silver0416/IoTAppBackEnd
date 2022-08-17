from django.urls import path, include, re_path
from rest_framework.authtoken import views
from .views import *
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet
from .viewsets import *
# urlpatterns = [
#     path('auth/api', include(router.urls)),
#     path('auth/', include('djoser.urls')),
#     path('auth/', include('djoser.urls.authtoken')),
#     path('activation/<str:uid>/<str:token>/', request_user_activation, name='request_user_activation'),
#     path('activation/<str:uid>/<str:token>/',
#          request_user_activation,
#          name='request_user_activation'),
#     path('password/reset/<str:uid>/<str:token>/',
#          reset_user_password,
#          name='reset_user_password'),
# #     path('chat/<str:room_name>/', room, name='room'),
# #     path('chat/', index, name='index'),
# ] 


router = DefaultRouter()
# router.register('user_belong_home', user_homeViewSet)
router.register("home_list", homeViewSet)
router.register("home_admin", homeAdminViewSet)
router.register("added_device_list", added_device_listViewSet)
router.register("device_type", device_typeViewSet)
router.register("category", categoryViewSet)
router.register("device_data", device_dataViewSet)
router.register("users", UserViewSet)
app_name = "api"

urlpatterns = [
    path("auth/", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path(
        "activation/<str:uid>/<str:token>/",
        request_user_activation,
        name="request_user_activation",
    ),
    path(
        "password/reset/<str:uid>/<str:token>/",
        reset_user_password,
        name="reset_user_password",
    ),
    #     re_path('^auth/home_list/$', homeViewSet.as_view()),
    #     path('chat/<str:room_name>/', room, name='room'),
    #     path('chat/', index, name='index'),
]
