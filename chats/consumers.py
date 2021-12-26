import json

from channels.generic.websocket import AsyncWebsocketConsumer

websockets = {}
bundles = {}
devices = {}


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.username = ''
        self.room_name, self.room_group_name = None, None
        super().__init__()

    async def connect(self):
        self.room_name = "room"
        self.room_group_name = f'chat_room'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        msg_type = message['type']

        if msg_type == 'register':
            user = message['user']
            self.username = user.username
            if self.username in websockets:
                websockets[self.username].append(self)
            else:
                websockets[self.username] = [self]
            devs = devices[self.username] if self.username in devices else []

            await self.send(text_data=json.dumps({
                'type': 'registered',
                'devices': devs,
            }))
            for dev in set(devs) - {self.username}:
                await self.send(text_data=json.dumps({
                    'type': 'devices',
                    'devices': devices[dev],
                    'username': dev,
                }))

        elif msg_type == 'bundle':
            bundles[message["deviceId"]] = message['bundle']

        elif msg_type == 'devices':
            devices[message["username"]] = message['devices']
            for user in websockets:
                if user != message["username"]:
                    websockets[user].send(text_data=json.dumps(message))

        elif msg_type == 'getBundle':
            if message["deviceId"] in bundles:
                await self.send(json.dumps({
                    "type": "bundle",
                    "deviceId": message["deviceId"],
                    "bundle": bundles[message["deviceId"]]
                }))

        elif msg_type == 'message':
            if message["to"] not in websockets:
                return

            for socket in websockets[message["to"]]:
                socket.send(json.dumps(message))
