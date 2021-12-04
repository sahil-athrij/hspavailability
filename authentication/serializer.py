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
    invited = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', "first_name", "last_name", 'tokens', 'friends', 'invited')

    def get_invited(self, user):
        friends = [{"name": tkn.user.username, "email": tkn.user.email, "profile": get_image(tkn)} for tkn in
                   Tokens.objects.filter(invite_token=user.tokens.private_token)]
        return friends

    def get_friends(self, user):
        friends = [{"name": user.username, "email": user.email, "profile": get_image(user.tokens)} for user in
                   user.tokens.friends.all()]
        return friends


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
