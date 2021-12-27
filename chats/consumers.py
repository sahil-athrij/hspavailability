import json

from channels.generic.websocket import AsyncWebsocketConsumer

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
        websockets.pop(self.username)
        devices.pop(self.username)

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        msg_type = message['type']

        if msg_type == 'register':
            self.username = message['username']
            websockets[self.username] = [*(websockets[self.username] if self.username in websockets else []), self]
            devs = devices[self.username] if self.username in devices else []

            await self.send(text_data=json.dumps({
                'type': 'registered',
                'devices': devs,
            }))

            for dev in set(devices) - {message['username']}:
                print(dev)
                await self.send(text_data=json.dumps({
                    'type': 'devices',
                    'devices': devices[dev],
                    'username': message['username'],
                }))

        elif msg_type == 'bundle':
            bundles[message["deviceId"]] = message['bundle']

        elif msg_type == 'devices':
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
            if message["to"] not in websockets:
                return

            print("Sending", message)

            for socket in websockets[message["to"]]:
                await socket.send(json.dumps(message))
