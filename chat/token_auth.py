
from channels.db import database_sync_to_async
from django.contrib.auth.models import User,AnonymousUser
from knox.models import AuthToken

@database_sync_to_async
def get_user(token):
    token = token.decode("utf-8")
    try:
        user = AuthToken.objects.get(token_key=token[0:8])
        return user.user
    except User.DoesNotExist:
        return AnonymousUser()

class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        coocie = (scope['headers'][10])
        token = coocie[1].split(b"Authorization=",1)[1] 
        print(coocie)
        
        scope['user'] = await get_user(token)

        return await self.app(scope, receive, send)