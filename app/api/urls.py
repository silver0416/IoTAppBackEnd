from allauth.account.views import confirm_email
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from .router import router


urlpatterns = [
    path('', include(router.urls)),
    path('auth/',include('djoser.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]