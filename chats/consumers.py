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
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(self.scope['user'])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = json.loads(event)
        msg_type = message['type']
        device_id = message['deviceId']
        if msg_type == 'register':
            user = message['user']
            self.username = user.username
            if self.username in websockets.keys():
                websockets[self.username].push(self)
            else:
                websockets[self.username] = [self]
            devs = devices[self.username] if self.username in devices.keys() else []

            await self.send(text_data=json.dumps({
                'type': 'registered',
                'devices': devs,
            }))
            for dev in devs:
                if dev == self.username:
                    continue
                await self.send(text_data=json.dumps({
                    'type': 'devices',
                    'devices': devices[dev],
                    'username': dev,
                }))
        elif msg_type == 'bundle':
            bundles[device_id] = message['bundle']
        elif msg_type == 'devices':
            devices[device_id] = message['devices']

    def sedToAll(self, ws, message):
        for key in websockets:
            self.sendToUserSockets(ws, key, message)

    def sendToUserSockets(self, ws, key, message):
        userSockets = websockets[key]
        badSockets = []

        for i in range(len(userSockets)):
            websocket = userSockets[i]

            if websocket == ws:
                continue
            websocket.send(text_data=json.dumps({
                message
            }))
            if len(badSockets) == len(userSockets):
                del websockets[i]
                return
            if len(userSockets) > 0:
                websocket[key] = userSockets
                return
            del websockets[key]
