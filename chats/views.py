from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from chats.models import ChatUser
from .serializers import ChatUserSerializer


class ChatUserApiViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ChatUserSerializer

    queryset = ChatUser.objects.all()
    http_method_names = ['get', 'post', 'options']

    def get_queryset(self):
        return ChatUser.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user, _ = ChatUser.objects.get_or_create(user=request.user)
        return Response(data=user, status=status.HTTP_200_OK)
