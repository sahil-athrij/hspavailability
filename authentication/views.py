from django.contrib.auth.models import User, Group
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from rest_framework_social_oauth2.authentication import SocialAuthentication
from .authentication import CsrfExemptSessionAuthentication
from .permissions import IsOwner
from .serializer import UserSerializer, GroupSerializer
from home.models import Language


class UserApiViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = UserSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, SocialAuthentication, OAuth2Authentication]
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    parser_class = [FileUploadParser]
    
    def get_queryset(self):
        try:
            return User.objects.filter(id=self.request.user.id)
        except User.DoesNotExist:
            return User.objects.none()
        except Exception:

            return User.objects.none()

    def list(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            self.queryset = self.queryset.filter(pk=request.user.pk)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    @action(detail=False, methods=["get", "post","patch"], url_path='me')
    def me(self, request, *args, **kwargs):
        if request.method == "PATCH":
            
            data = request.data
            user = request.user
            languages = request.data.get('languages')
            token = user.tokens
            try:
                profile = request.FILES['image']
                token.profile=profile
            except:
                pass

            print(languages)
            if languages:
                for ln in languages:
                    lang_obj,_ = Language.objects.get_or_create(name=ln.lower())
                    token.language.add(lang_obj.id)
            token.save()

            serializer = UserSerializer(user, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
        else:
            self.queryset = self.queryset.filter(pk=request.user.pk)
            return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
