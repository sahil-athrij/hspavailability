from rest_framework import serializers

from internals.serializers import GetImageSerializer, GetBuildingSerializer, DoctorSerializer,GetDepartmentSerializer
from .models import Markers, Reviews, SuspiciousMarking, Patient, Tokens, Spoken_Language, Language
from internals.models import ProfileImage
from maps.settings import DEPLOYMENT_URL


class GetMarkerSerializer(serializers.ModelSerializer):
    images = GetImageSerializer(many=True, required=False, read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Markers
        fields = [
            'id', 'name', 'Phone', 'size', 'financial_rating', 'avg_cost', 'covid_rating', 'beds_available',
            'care_rating', 'oxygen_rating', 'ventilator_availability', 'oxygen_availability', 'icu_availability',
            'lat', 'lng', 'datef', 'added_by_id', 'images', 'display_address', 'comment_count', 'address',
            'pending_approval', 'category', 'type', 'ownership', 'about',
        ]
        extra_kwargs = {
            'pending_approval': {'read_only': True},
            'size': {'read_only': True},
            'financial_rating': {'read_only': True},
            'avg_cost': {'read_only': True},
            'covid_rating': {'read_only': True},
            'beds_available': {'read_only': True},
            'care_rating': {'read_only': True},
            'oxygen_rating': {'read_only': True},
            'ventilator_availability': {'read_only': True},
            'oxygen_availability': {'read_only': True},
            'icu_availability': {'read_only': True},
            'datef': {'read_only': True},
            'added_by_id': {'read_only': True},
            'address': {'read_only': True}
        }

    def get_comment_count(self, marker):
        return marker.comment.all().count()


class GetReviewSerializer(serializers.ModelSerializer):
    images = GetImageSerializer(many=True, required=False)
    written_by_name = serializers.SerializerMethodField(read_only=True)
    written_by_profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reviews
        fields = [
            'id', 'marker', 'financial_rating','total_rating','avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating',
            'beds_available', 'size', 'ventilator_availability', 'oxygen_availability',
            'icu_availability', 'comment', 'written_by', 'images', 'written_by_name', 'datef','written_by_profile'

        ]


    def get_written_by_profile(self, obj):
        # Use a try - except block if needed
        try:
            img = DEPLOYMENT_URL + ProfileImage.objects.get(user_id=obj.written_by).image.url
        except ProfileImage.DoesNotExist:
            img = ''
        return img

    def get_written_by_name(self, review):
        return review.written_by.username


class GetSusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspiciousMarking
        fields = [
            'id', 'marker', 'comment', 'created_by_id', 'datef'
        ]


class GetPatientSerializer(serializers.ModelSerializer):
    gender_name = serializers.CharField(source='get_gender_display', read_only=True)
    bedtype_name = serializers.CharField(source='get_bedtype_display', read_only=True)
    helped_by_name = serializers.CharField(source='get_helped_by_display', read_only=True)
    class Meta:
        model = Patient
        fields = [
            'id', 'Name', 'age', 'gender', 'address', 'symptoms', 'symdays', 'spo2', 'oxy_bed', 'covidresult',
            'hospitalpref', 'attendername', 'attenderphone', 'relation', 'srfid', 'bunum', 'blood', 'bedtype', 'ct',
            'ctscore', 'category', 'ownership', 'gender_name', 'bedtype_name' ,'helped_by_name','helped_by'

        ]


class DetailMarkerSerializer(GetMarkerSerializer):
    comment = GetReviewSerializer(read_only=True, required=False, many=True)
    buildings = GetBuildingSerializer(read_only=True, required=False, many=True)
    doctors = DoctorSerializer(read_only=True, required=False, many=True,)
    departments = GetDepartmentSerializer(many=True, read_only=True)

    class Meta(GetMarkerSerializer.Meta):
        fields = GetMarkerSerializer.Meta.fields + ['comment', 'buildings', 'doctors',"departments"]


class GetTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = [
            'user', 'private_token', 'invite_token', 'invited', 'points', 'reviews', 'reports'
        ]


class Language_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = [
            'name'
        ]


class SpokenLanguages_Serializers(serializers.ModelSerializer):

    # language = Language_Serializer(many=True)
    class Meta:
        model = Spoken_Language
        fields = [
            'language'
        ]