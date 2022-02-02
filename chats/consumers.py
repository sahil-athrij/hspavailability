import json
from datetime import datetime
from logging import getLogger

import redis
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser, User

from maps import settings
from .models import Bundle, Devices

websockets = {}

logger = getLogger('home')
db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


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

        logger.debug(f"Letting the world know {self.device_id} has joined the party!")
        for key in websockets:  # TODO Don't do this
            await websockets[key].send(text_data=json.dumps(message))

        websockets[(self.username, self.device_id)] = self

        msgs = db.smembers(str((self.username, self.device_id)))
        logger.debug(f"Sending {len(msgs)} messages")

        for msg in msgs:
            try:
                await self.send(msg)
                db.srem(msg)
            except Exception as e:
                logger.exception(e)

        logger.debug("All previous message sent to device. Redis should be cleared")

    async def bundle(self, message):
        await self.set_bundle(message["username"], message['bundle'], message['deviceId'])

    async def get_bundle(self, message):
        bundle = await self.get_bundle_from_db(message['deviceId'], message['username'])
        if bundle:
            logger.debug(f"Sending bundle {message['deviceId'], message['username'] =} to {self.username =}")
            await self.send(json.dumps({
                "type": "bundle",
                "deviceId": bundle.deviceId,
                "bundle": bundle.data,

            }))
        else:
            logger.error(f"Bundle for {message['deviceId'], message['username'] =} not found.")

    async def message(self, message):
        to_send = await self.get_to_send(message)
        message = json.dumps(message)

        logger.debug(f"Sending message to {to_send}")

        for key in to_send:
            if key in websockets:
                await websockets[key].send(message)
            else:
                db.sadd(str(key), message)

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        handlers = {"message": self.message, "getBundle": self.get_bundle, "bundle": self.bundle,
                    "devices": self.devices, "register": self.register}

        if message['type'] in handlers:
            logger.info(f"Processing message of type {message['type']}")
            await handlers[message['type']](message)
        else:
            logger.error(f"Unknown request type {message['type'] = }")

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
    def create_devices(self, username, devs):
        device, _ = Devices.objects.get_or_create(username=username)
        logger.info(f"Existing devices, {device.data}")
        if device.data != devs:
            logger.info(f"New device registered, device id = {set(devs)-set(device.data or [])}")
            device.data = devs
            device.save()

        return device

    @database_sync_to_async
    def get_to_send(self, data):
        to_devs = Devices.objects.get(username=data["to"]).data
        to_send = []

        for d in data["encrypted"]["header"]["keys"]:
            user = data["to"] if d["rid"] in to_devs else self.username
            to_send.append((user, d["rid"]))

        return to_send

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
