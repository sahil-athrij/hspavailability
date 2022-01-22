from django.contrib.auth.models import User, Group
from rest_framework import serializers

from chats.models import Bundle, ChatUser
from home.models import Tokens
from home.serializer import GetTokensSerializer


def get_image(token):
    if token.profile:
        return token.profile.url
    return ""


class UserSerializer(serializers.ModelSerializer):
    tokens = GetTokensSerializer(many=False, read_only=True, required=False)
    friends = serializers.SerializerMethodField()
    chat_friends = serializers.SerializerMethodField()
    invited = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', "first_name", "last_name", 'tokens', 'friends', 'invited', 'chat_friends')

    def get_invited(self, user):
        friends = [{"name": tkn.user.username, "email": tkn.user.email, "profile": get_image(tkn)} for tkn in
                   Tokens.objects.filter(invite_token=user.tokens.private_token)]
        return friends

    def get_friends(self, user):
        friends = [{"name": user.username, "email": user.email, 'token': user.tokens.private_token,
                    "profile": get_image(user.tokens)} for user in
                   user.tokens.friends.all()]
        return friends

    def get_chat_friends(self, user):
        friends = [{"name": user.username, "email": user.email, 'token': ChatUser.objects.filter(user=user).first().id,
                    "profile": get_image(user.tokens)} for
                   user in
                   user.tokens.friends.all() if Bundle.objects.filter(
                user__user__tokens=user.tokens).exists()]
        print(f"{friends = }")


        return friends


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
