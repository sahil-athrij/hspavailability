import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maps.settings")
django.setup()

import chats.routing
from chats.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
        TokenAuthMiddleware(
            URLRouter(
                chats.routing.websocket_urlpatterns
            )
        ),
})
