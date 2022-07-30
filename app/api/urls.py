from allauth.account.views import confirm_email
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from dj_rest_auth.registration.views import VerifyEmailView
from .router import router


urlpatterns = [
    path('', include(router.urls)),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/',include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]