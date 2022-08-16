from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.db import close_old_connections


@database_sync_to_async
def get_user(headers):
    try:
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'Token':
                token = Token.objects.get(key=token_key)
                print(token.user)
                return token.user
        else:
            raise Token.DoesNotExist
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        headers = dict(scope['headers'])
        if b'authorization' in headers:
            scope['user'] = await get_user(headers)
        else:
            scope['user'] = AnonymousUser()
        return await self.inner(scope, receive, send)

# TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(
#     AuthMiddlewareStack(inner))
