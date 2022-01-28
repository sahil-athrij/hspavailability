import json
from logging import getLogger

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import ChatUser, Bundle, Devices, Message

websockets = {}

logger = getLogger('chat')


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.username = ''
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

        if self.username:

            try:
                logger.info(f'popping {self.username} from websockets')
                websockets.pop(self.username)
            except KeyError:
                logger.info(f"{self.username} not found on websockets")
            # try:
            #     await self.delete_user_device(self.username)
            # except KeyError:
            #     logger.info(f"{self.username} not found on device")

    async def receive(self, text_data=None, bytes_data=None):
        logger.info('received data from websocket ')
        message = json.loads(text_data)
        logger.info(f"{message = }")
        user = self.scope['user']
        logger.info(user)
        msg_type = message['type']
        logger.info(f"{msg_type = }")
        if msg_type == 'register':
            user = await self.get_user(message["username"])
            self.username = user.id
            logger.info(f"registering user account {self.username}")
            websockets[self.username] = [*(websockets[self.username] if self.username in websockets else []), self]
            logger.debug(f"now websockets {websockets = }")
            logger.info('getting the details of devices')
            devs = await self.get_devices(self.username)
            logger.info(f'{devs = }')

            if devs:
                devs = devs.data
            else:
                devs = []
            logger.info(f'sending devices list to {self.username} ')
            await self.send(text_data=json.dumps({
                'type': 'registered',
                'devices': devs,
            }))
            logger.info(f"getting get all devices except {self.username}'s ")

            devices = await self.get_all_devices_except_mine(self.username)

            logger.info(f"{devices =}")

            for dev in devices:
                logger.info(f"{dev = }")
                await self.send(text_data=json.dumps({
                    'type': 'devices',
                    'devices': dev.data,
                    'username': dev.username,
                }))
            logger.info(f'devices sent')
            logger.info(f'getting msgs to {self.username}')
            msgs = await self.get_msgs(self.username)
            if msgs:
                logger.info('msgs ')
                logger.info(f"{msgs = }")
            for msg in msgs:
                logger.info(f'sending msg {msg.data}')
                await self.send(json.dumps(msg.data))
            await self.delete_msgs(self.username)

        elif msg_type == 'bundle':
            logger.info('sending bundle')
            logger.info(f'{message = }')
            user = await self.get_user(message["username"])
            b = await self.set_bundle(user, message['bundle'], message['deviceId'])
            logger.info(b)
            logger.info('set bundle called')

        elif msg_type == 'devices':
            logger.info('got req to devices')
            await self.create_devices(message['username'], message['devices'])

            for user in websockets:
                if user != self.username:
                    for socket in websockets[user]:
                        await socket.send(text_data=json.dumps(message))

        elif msg_type == 'getBundle':
            logger.info('get bundle called')
            logger.info(message)
            bundle = await self.get_bundle(message['deviceId'])
            logger.info(bundle)
            logger.info('sending bundle')
            if bundle:
                await self.send(json.dumps({
                    "type": "bundle",
                    "deviceId": bundle.deviceId,
                    "bundle": bundle.data,

                }))

        elif msg_type == 'message':
            logger.info(f"trying to send message to {message['to']} from {self.username}")
            if message["to"] not in websockets:
                await self.create_msgs(message, message['to'])
                logger.info(message["to"], "Not found in websockets")
            else:
                try:
                    for socket in websockets[message["to"]]:
                        await socket.send(json.dumps(message))
                except Exception as e:
                    logger.exception(e)
                    await self.create_msgs(message, message['to'])
                    logger.info(f'(message["to"], f" websocket error {e}"')
        else:
            logger.info("Unknown message type", message)

    @database_sync_to_async
    def get_user(self, uid):
        return ChatUser.objects.get(id=uid)

    @database_sync_to_async
    def set_bundle(self, user, data, device_id):
        logger.info('setting bundle')
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
        logger.info('deleting mss')

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
