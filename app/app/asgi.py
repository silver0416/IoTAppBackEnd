"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter
import os
import api.routing
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from api.token_auth import TokenAuthMiddleware
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http":
    django_asgi_app,
    "websocket":
    AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(api.routing.websocket_urlpatterns))),
    # 'websocket':
    # TokenAuthMiddleware(URLRouter(api.routing.websocket_urlpatterns)),
})
