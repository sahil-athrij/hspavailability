import json
from datetime import datetime
from logging import getLogger
from typing import List

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser, User

from .models import Bundle, Devices, Message

websockets = {}

logger = getLogger('home')


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.username = ''
        self.device_id = ''
        self.user = AnonymousUser()
        logger.info('chat consumer initialisation')
        super().__init__()

    async def connect(self):
        self.user = self.scope['user']
        logger.info('connecting')
        # if self.user.is_authenticated:
        logger.info('accepting')
        await self.accept()

    async def disconnect(self, code):
        logger.info(f'websocket Disconnect from {self.username = } , {code = }')
        (self.username, self.device_id) in websockets and websockets.pop((self.username, self.device_id))

    async def register(self, message):
        self.username = message["username"]
        devs = await self.get_devices(self.username)

        await self.send(text_data=json.dumps({
            'type': 'registered',
            'devices': devs.data if devs else [],
        }))

        devices = await self.get_all_devices_except_mine(self.username)

        for dev in devices:
            logger.info(f"{dev = }")
            await self.send(text_data=json.dumps({
                'type': 'devices',
                'devices': dev.data,
                'username': dev.username,
            }))

    async def devices(self, message):
        self.device_id = message['ownDeviceId']
        await self.create_devices(message['username'], message['devices'])

        for key in websockets:  # TODO Don't do this
            await websockets[key].send(text_data=json.dumps(message))

        websockets[(self.username, self.device_id)] = self
        return self.send_message(await self.get_msgs(self.username))

    async def bundle(self, message):
        return self.set_bundle(message["username"], message['bundle'], message['deviceId'])

    async def get_bundle(self, message):
        bundle = await self.get_bundle_from_db(message['deviceId'], message['username'])
        if bundle:
            logger.info('sending bundle')
            await self.send(json.dumps({
                "type": "bundle",
                "deviceId": bundle.deviceId,
                "bundle": bundle.data,

            }))

    async def message(self, message):
        return await self.send_message(await self.create_msgs(message, message['to']))

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        handlers = {"message": self.message, "getBundle": self.get_bundle, "bundle": self.bundle,
                    "devices": self.devices, "register": self.register}

        if message['type'] in handlers:
            await handlers[message['type']](message)
        else:
            logger.error(f"Unknown request type {message['type'] = }")

    async def send_message(self, *msgs):
        for msg in msgs:
            for key in msg.to_send:
                if tuple(key) in websockets:
                    await websockets[tuple(key)].send(json.dumps(msg.data))
                    await self.pop_from_to_send(msg, key)

    @database_sync_to_async
    def set_last_seen(self, uid):
        user = User.objects.get(tokens__private_token=uid)
        user.tokens.last_seen = datetime.now()
        user.save()

    @database_sync_to_async
    def set_bundle(self, token, data, device_id):
        bundle, _ = Bundle.objects.get_or_create(user=User.objects.get(tokens__private_token=token), deviceId=device_id)
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
        to_devs = Devices.objects.get(username=to_user_id).data
        to_send = [[to_user_id if d["rid"] in to_devs else self.username, d["rid"]] for d in
                   data["encrypted"]["header"]["keys"]]

        return Message.objects.create(data=data, to_user_id=to_user_id, to_send=to_send)

    @database_sync_to_async
    def get_msgs(self, to_user_id) -> List[Message]:
        msg = list(Message.objects.filter(to_user__tokens__private_token=to_user_id, ))
        return msg

    @database_sync_to_async
    def get_devices(self, username):
        return Devices.objects.filter(username=username).first()

    @database_sync_to_async
    def get_bundle_from_db(self, device_id, username):
        bundle = Bundle.objects.filter(deviceId=device_id, user__tokens__private_token=username).first()
        return bundle or Bundle.objects.filter(deviceId=device_id, user__tokens__private_token=self.username).first()

    @database_sync_to_async
    def delete_user_device(self, username):
        Devices.objects.filter(username=username).delete()

    @database_sync_to_async
    def get_all_devices_except_mine(self, username):
        return list(Devices.objects.all().exclude(username=username))

    @database_sync_to_async
    def pop_from_to_send(self, msg: Message, key):
        msg.to_send.remove(key)
        (msg.delete if not len(msg.to_send) else msg.save)()
