
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chats.routing
from chats.middleware import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maps.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        TokenAuthMiddleware(
            URLRouter(
                chats.routing.websocket_urlpatterns
            )
    ),
})
