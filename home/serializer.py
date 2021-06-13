from rest_framework import serializers

from .models import Images, Markers, Reviews, SuspiciousMarking, Patient


class getImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image', 'useinmarker'
        ]


class getMarkerSerializer(serializers.ModelSerializer):
    images = getImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Markers
        fields = [
            'id', 'name', 'Phone', 'size', 'financial_rating', 'avg_cost', 'covid_rating', 'beds_available',
            'care_rating', 'oxygen_rating', 'ventilator_availability', 'oxygen_availability', 'icu_availability',
            'lat', 'lng', 'datef', 'added_by_id', 'images', 'display_address'
        ]
        extra_kwargs = {
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
            'added_by_id': {'read_only': True}
        }


class getReviewSerializer(serializers.ModelSerializer):
    images = getImageSerializer(many=True, required=False)

    class Meta:
        model = Reviews
        fields = [
            'id', 'marker', 'financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating',
            'beds_available', 'size', 'ventilator_availability', 'oxygen_availability',
            'icu_availability', 'comment', 'written_by', 'images'
        ]


class getSusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspiciousMarking
        fields = [
            'id', 'marker', 'comment', 'created_by_id', 'datef'
        ]

class getPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'Name', 'age', 'gender', 'symptoms', 'symdays', 'spo2', 'hospitalday', 'covidresult', 'hospitalpref',
            'attendername', 'attenderphone', 'relation', 'srfid', 'bunum', 'blood', 'bedype', 'ct', 'ctscore'
        ]