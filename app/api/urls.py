from django.urls import path, include, re_path
from rest_framework.authtoken import views
from .views import *
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet
from .viewsets import *

router = DefaultRouter()
# router.register('user_belong_home', user_homeViewSet)
router.register("home_list", homeViewSet)
router.register("home_admin", homeAdminViewSet)
router.register("add_device", add_deviceViewSet)
router.register("device_data", device_dataViewSet)
router.register("users", UserViewSet)
router.register("mode_key_data", mode_key_dataViewSet)
router.register("chat_room_data", chat_room_dataViewSet)
router.register("chat_room", chat_roomViewSet)
app_name = "api"    

urlpatterns = [
    path("auth/", include(router.urls)),
    # path("auth/", include("djoser.urls")),
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
    path("chat/<str:room_name>/", room, name="room"),
    path("chat/", index, name="index"),
]
