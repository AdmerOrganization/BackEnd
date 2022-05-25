# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing
from chat.token_auth import QueryAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_backend.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": QueryAuthMiddleware(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})