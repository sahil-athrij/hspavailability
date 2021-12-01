from rest_framework import serializers

from .models import KeyExchange


class KeyExchangeSerializer(serializers.ModelSerializer):
    sender_token = serializers.SerializerMethodField()
    receiver_token = serializers.SerializerMethodField()

    class Meta:
        model = KeyExchange
        fields = [
            'sender_token', 'receiver_token', 'receiver_key_bundle', 'sender_key_bundle',
        ]

    def get_sender_token(self, key):
        return key.sender.tokens.private_token

    def get_receiver_token(self, key):
        return key.receiver.tokens.private_token
