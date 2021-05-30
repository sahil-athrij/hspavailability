from rest_framework import serializers
from .models import Images, Markers, Reviews


class getImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image', 'useinmarker'
        ]


class getMarkerSerializer(serializers.ModelSerializer):
    images = getImageSerializer(many=True, required=False)

    class Meta:
        model = Markers
        fields = [
            'id', 'name', 'Phone', 'size', 'financial_rating', 'avg_cost', 'covid_rating', 'beds_available',
            'care_rating', 'oxygen_rating', 'ventilator_availability', 'oxygen_availability', 'icu_availability',
            'images'
        ]


class getReviewSerializer(serializers.ModelSerializer):
    images = getImageSerializer(many=True, required=False)

    class Meta:
        model = Reviews
        fields = [
            'ids', 'M_id', 'fin', 'cost', 'covid', 'care', 'oxy', 'beds', 'vent', 'oxya', 'icu', 'comment', 'written',
            'images'
        ]
