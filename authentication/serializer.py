from django.contrib.auth.models import User, Group
from home.serializer import GetTokensSerializer
from rest_framework import serializers
from internals.models import Images


class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image'
        ]

# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    tokens = GetTokensSerializer(many=False, read_only=True, required=False)
    uploaded_images = GetImageSerializer(many=True)
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name", 'tokens','uploaded_images')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
