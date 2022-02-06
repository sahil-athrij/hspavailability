import json
from logging import getLogger

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from typing import Dict, List, Any

from maps import settings

logger = getLogger('main')

TYPE_OFFER = "OFFER"
TYPE_ANSWER = "ANSWER"
TYPE_ICECANDIDATE = "ICE CANDIDATE"
TYPE_CALL_REJECT = "REJECT CALL"
TYPE_REGISTER = "REGISTER"
TYPE_CALL_END = "END CALL"


@database_sync_to_async
def send_push_notification(from_user, to_user):
    """
        Get the subscription object of the user from db and send a push notification using it.
        Somebody should probably receive and store subscription object from user first.
    """
    return settings.NOTIFICATION_KEY + from_user + to_user  # TODO: I think we should actually send notification


class Consumer(AsyncWebsocketConsumer):
    user: AnonymousUser
    to: str
    token: str

    def __init__(self):
        super().__init__()
        self.user = AnonymousUser()

    async def connect(self):
        self.user = self.scope['user']
        # if self.user.is_authenticated:
        logger.info(f"Connected to {self.user.username =}")
        await self.accept()

    async def disconnect(self, code):
        logger.info(f'websocket Disconnect from {self.token} , {code = }')
        websockets.pop(self.token)
        if self.to in websockets:
            await websockets[self.to].send_message({
                "type": TYPE_CALL_END,
                "data": "Good Bye 👋",
                "metadata": {"to": self.token}
            })

    async def send_message(self, message):
        if message["type"] in [TYPE_OFFER, TYPE_ANSWER, TYPE_ICECANDIDATE, TYPE_CALL_REJECT, TYPE_CALL_END]:
            await self.send(text_data=json.dumps({
                "type": message["type"],
                "data": message["data"],
                "error": message["error"] if "error" in message else None,
                "metadata": {
                    "token": self.token,
                    "from": message["metadata"]["to"]
                }
            }))
        else:
            logger.error(f'Invalid message of type { message["type"]} from {message["metadata"]["to"]}')

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)

        logger.info(f"Received message of type {message['type']} from {message['metadata']['token']}")

        if message["type"] == TYPE_CALL_REJECT:
            message["error"] = message["data"]

        if message["type"] == TYPE_REGISTER:
            self.token = message["metadata"]["token"]
            self.to = message["metadata"]["to"]

            websockets[self.token] = self

            if self.token in messages:
                for msg in messages[self.token]:
                    await self.send_message(msg)
                messages[self.token] = []

        elif self.to in websockets:
            await websockets[self.to].send_message(message)
        else:
            if message["type"] == TYPE_OFFER:
                await send_push_notification(message["metadata"]["token"], message["metadata"]["to"])

            messages[self.to] = [*message[self.to], message] if self.to in messages else [message]


websockets: Dict[str, Consumer] = {}
messages: Dict[str, List[Any]] = {}
