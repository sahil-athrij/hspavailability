import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatUser

websockets = {}
bundles = {}
devices = {}


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.username = ''

        super().__init__()

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        print('Disconnect from', self.username, code)

        if self.username:
            try:
                websockets.pop(self.username)
            except KeyError:
                print(f"{self.username} not found on websockets")
            try:
                devices.pop(self.username)
            except KeyError:
                print(f"{self.username} not found on device")

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        user = self.scope['user']
        print(user)
        # print(f"{self.user = }")
        msg_type = message['type']
        if msg_type == 'register':

            user = await self.get_user(message["username"])
            self.username = user.id
            websockets[self.username] = [*(websockets[self.username] if self.username in websockets else []), self]
            devs = devices[self.username] if self.username in devices else []


            await self.send(text_data=json.dumps({
                'type': 'registered',
                'devices': devs,
            }))
            print("send the devs")

            for dev in set(devices) - {message['username']}:
                await self.send(text_data=json.dumps({
                    'type': 'devices',
                    'devices': devices[dev],
                    'username': message['username'],
                }))

        elif msg_type == 'bundle':
            # Bundle.objects.create(data=message['bundle'])
            bundles[message["deviceId"]] = message['bundle']

        elif msg_type == 'devices':
            # Devices.objects.create(data=message['devices'])
            devices[message["username"]] = message['devices']

            for user in websockets:
                if user != message["username"]:
                    for socket in websockets[user]:
                        await socket.send(text_data=json.dumps(message))

        elif msg_type == 'getBundle':
            if message["deviceId"] in bundles:
                await self.send(json.dumps({
                    "type": "bundle",
                    "deviceId": message["deviceId"],
                    "bundle": bundles[message["deviceId"]]
                }))

        elif msg_type == 'message':
            print(f'{message = }')
            if message["to"] not in websockets:
                return print(message["to"], "Not found")
            ids = []
            for i in message['encrypted']['header']['keys']:
                if i['rid'] != message['encrypted']['header']['sid']:
                    ids.append(i)
            # message['encrypted']['header']['keys'] = ids
            print(f'{message = }')
            for socket in websockets[message["to"]]:
                await socket.send(json.dumps(message))

        else:
            print("Unknown message type", message)

    @database_sync_to_async
    def get_user(self, uid):
        return ChatUser.objects.get(id=uid)
