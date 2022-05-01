from django.conf.urls import url

from .consumers import call_consumer, message_consumer

websocket_urlpatterns = [
    url('chat/webrtc', call_consumer.Consumer.as_asgi()),
    url('chat/message', message_consumer.Consumer.as_asgi()),
]
