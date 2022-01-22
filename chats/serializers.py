from rest_framework import serializers

from .models import ChatUser


class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ("id", 'device_ids', 'user')
        extra_kwargs = {
            'id': {'read_only': True},
            'device_ids': {'read_only': True},
            'user': {'read_only': True},
        }
