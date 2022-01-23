import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import ChatUser, Bundle, Devices, Message

websockets = {}


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.username = ''
        self.user = AnonymousUser()

        super().__init__()

    async def connect(self):
        self.user = self.scope['user']
        # if self.user.is_authenticated:
        await self.accept()

    async def disconnect(self, code):
        print('Disconnect from', self.username, code)

        if self.username:
            try:
                websockets.pop(self.username)
            except KeyError:
                print(f"{self.username} not found on websockets")
            # try:
            #     await self.delete_user_device(self.username)
            # except KeyError:
            #     print(f"{self.username} not found on device")

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        # user = self.scope['user']
        # print(user)
        msg_type = message['type']
        if msg_type == 'register':

            user = await self.get_user(message["username"])
            self.username = user.id
            websockets[self.username] = [*(websockets[self.username] if self.username in websockets else []), self]
            devs = await self.get_devices(self.username)
            if devs:
                devs = devs.data
            else:
                devs = []

            await self.send(text_data=json.dumps({
                'type': 'registered',
                'devices': devs,
            }))
            print("send the devs")

            devices = await self.get_all_devices_except_mine(self.username)
            for dev in devices:
                print(f"{dev = }")
                await self.send(text_data=json.dumps({
                    'type': 'devices',
                    'devices': dev.data,
                    'username': dev.username,
                }))
            msgs = await self.get_msgs(self.username)
            print(f"{msgs = }")
            for msg in msgs:
                print(f'sending msg {msg.data}')
                await self.send(json.dumps(msg.data))
            await self.delete_msgs(self.username)

        elif msg_type == 'bundle':
            # print('sending bundle')
            # print(f'{message = }')
            user = await self.get_user(message["username"])
            b = await self.set_bundle(user, message['bundle'], message['deviceId'])
            # print(b)
            print('set bundle called')

        elif msg_type == 'devices':
            print('got req to devices')
            await self.create_devices(message['username'], message['devices'])

            for user in websockets:
                if user != self.username:
                    for socket in websockets[user]:
                        await socket.send(text_data=json.dumps(message))

        elif msg_type == 'getBundle':
            # print('get bundle')
            # print(message)
            bundle = await self.get_bundle(message['deviceId'])
            # print(bundle)
            # print('sending bundle')
            if bundle:
                await self.send(json.dumps({
                    "type": "bundle",
                    "deviceId": bundle.deviceId,
                    "bundle": bundle.data,

                }))

        elif msg_type == 'message':
            print(f"trying to send message to {message['to']} from {self.username}")
            if message["to"] not in websockets:
                await  self.create_msgs(message, message['to'])
                print(message["to"], "Not found in websockets")
            else:
                try:
                    for socket in websockets[message["to"]]:
                        await socket.send(json.dumps(message))
                except Exception as e:
                    print(e)
                    await  self.create_msgs(message, message['to'])
                    print(message["to"], f" websocket error {e}")
        else:
            print("Unknown message type", message)

    @database_sync_to_async
    def get_user(self, uid):
        return ChatUser.objects.get(id=uid)

    @database_sync_to_async
    def set_bundle(self, user, data, device_id):
        print('setting bundle')
        bundle, _ = Bundle.objects.get_or_create(user=user, deviceId=device_id)
        bundle.data = data
        bundle.save()

    @database_sync_to_async
    def create_devices(self, username, message):
        device, _ = Devices.objects.get_or_create(username=username)
        device.data = message
        device.save()

        return device

    @database_sync_to_async
    def create_msgs(self, data, to_user_id):
        msg = Message.objects.create(data=data, to_user_id=to_user_id, )
        return msg

    @database_sync_to_async
    def get_msgs(self, to_user_id):
        msg = list(Message.objects.filter(to_user_id=to_user_id, ))
        return msg

    @database_sync_to_async
    def delete_msgs(self, to_user_id):
        Message.objects.filter(to_user_id=to_user_id).filter().delete()
        print('deleting mss')

    @database_sync_to_async
    def get_devices(self, username):
        return Devices.objects.filter(username=username).first()

    @database_sync_to_async
    def get_bundle(self, device_id):
        return Bundle.objects.filter(deviceId=device_id).first()

    @database_sync_to_async
    def delete_user_device(self, username):
        Devices.objects.filter(username=username).delete()

    @database_sync_to_async
    def get_all_devices_except_mine(self, username):
        return list(Devices.objects.all().exclude(username=username))
