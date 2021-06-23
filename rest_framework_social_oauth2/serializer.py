from rest_framework import serializers


class TokensSerializer(serializers.Serializer, ):
    token = serializers.CharField(max_length=5000)
