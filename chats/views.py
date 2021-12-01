import logging

import django_filters
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.permissions import IsSenderOrReceiver
from home.models import Tokens
from .models import KeyExchange
from .serializers import KeyExchangeSerializer


def index(request):
    return render(request, 'chats/index.html', {})


def room(request, room_name):
    return render(request, 'chats/room.html', {
        'room_name': room_name
    })


class KeyExchangeViewSet(viewsets.ModelViewSet):
    serializer_class = KeyExchangeSerializer
    http_method_names = ['get', 'post', 'patch']
    queryset = KeyExchange.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [IsSenderOrReceiver]

    def get_queryset(self):

        return KeyExchange.objects.filter(sender=self.request.user)
        # try:
        #     receiver_token = self.request.data['receiver_token']
        #     token = Tokens.objects.get(private_token=receiver_token)
        #     return KeyExchange.objects.filter(sender=self.request.user,receiver=token.user)
        # except Tokens.DoesNotExist:
        #     pass
        # except Exception as e:
        #     logging.exception(e)
        # return KeyExchange.objects.none()

    def create(self, request, *args, **kwargs):
        receiver_token = request.user.tokens
        try:
            receiver_token = Tokens.objects.get(private_token=request.data['receiver_token'])
        except Tokens.DoesNotExist:
            Response({"detail": "receiver token is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        if receiver_token:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(sender=request.user, receiver=receiver_token.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"detail": "receiver token is not valid"}, status=status.HTTP_400_BAD_REQUEST)
