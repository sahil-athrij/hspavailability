from django.contrib.auth.models import User, Group
from home.serializer import GetTokensSerializer
from rest_framework import serializers
from internals.models import ProfileImage


# first we define the serializers
from maps.settings import DEPLOYMENT_URL


class UserSerializer(serializers.ModelSerializer):
    tokens = GetTokensSerializer(many=False, read_only=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name", 'tokens', 'image')

    def get_image(self, obj):
        # Use a try - except block if needed
        try:
            img = DEPLOYMENT_URL + ProfileImage.objects.get(user_id=obj.id).image.url
        except ProfileImage.DoesNotExist:
            img = ''
        return img


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
