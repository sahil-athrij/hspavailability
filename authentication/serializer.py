from django.contrib.auth.models import User, Group
from rest_framework import serializers

from home.models import Tokens
from home.serializer import GetTokensSerializer


# first we define the serializers
#
#
# class FriendSerialiser(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', "first_name", "last_name",)


def get_image(token):
    if token.profile:
        return token.profile.url
    return ""


class UserSerializer(serializers.ModelSerializer):
    tokens = GetTokensSerializer(many=False, read_only=True, required=False)
    friends = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', "first_name", "last_name", 'tokens', 'friends')

    def get_friends(self, user):
        friends = [{"name": tkn.user.username, "email": tkn.user.email, "profile": get_image(tkn)} for tkn in
                   Tokens.objects.filter(invite_token=user.tokens.private_token)]
        return friends


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
