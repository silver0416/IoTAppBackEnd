from django.urls import path, include, re_path
from rest_framework.authtoken import views
from .router import router
from .views import *

urlpatterns = [
    path('auth/api', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('activation/<str:uid>/<str:token>/', request_user_activation, name='request_user_activation'),
]