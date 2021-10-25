from django.contrib.auth.models import User, Group
from home.serializer import GetTokensSerializer,SpokenLanguages_Serializers
from rest_framework import serializers
from internals.models import ProfileImage
from home.models import Spoken_Language

# first we define the serializers
from maps.settings import DEPLOYMENT_URL


class UserSerializer(serializers.ModelSerializer):
    tokens = GetTokensSerializer(many=False, read_only=True, required=False)
    image = serializers.CharField(source='profile.image.url', read_only=True)
    spoken_language = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name", 'tokens', 'image', 'spoken_language')

    def get_image(self, obj):
        # Use a try - except block if needed
        try:
           img = DEPLOYMENT_URL + ProfileImage.objects.get(user_id=obj.id).image.url
        except ProfileImage.DoesNotExist:
            img = ''
        return img

    def get_spoken_language(self, obj):
        try:
            languages = Spoken_Language.objects.get(user_id=obj.id)
            lang = [ln.name for ln in languages.language.all()]
            return lang
        except Spoken_Language.DoesNotExist:
            return []

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
