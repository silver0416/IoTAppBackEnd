from django.urls import path, include, re_path
from rest_framework.authtoken import views
from .router import router
from .views import *
urlpatterns = [
    path('auth/api', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('activation/<str:uid>/<str:token>/', request_user_activation, name='request_user_activation'),
    path('activation/<str:uid>/<str:token>/',
         request_user_activation,
         name='request_user_activation'),
    path('password/reset/<str:uid>/<str:token>/',
         reset_user_password,
         name='reset_user_password'),
] 