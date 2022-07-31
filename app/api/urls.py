from allauth.account.views import  EmailVerificationSentView as TemplateView
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView, LoginView
from .router import router


urlpatterns = [
    path('', include(router.urls)),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('n/',include('dj_rest_auth.registration.urls')),
    path('login/', LoginView.as_view(), name='account_login'),
    path('registration/', RegisterView.as_view(), name='account_signup'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    re_path(r'^/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),name='account_confirm_email'),
]