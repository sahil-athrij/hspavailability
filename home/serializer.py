from rest_framework import serializers

from .models import Images, Markers, Reviews, SuspiciousMarking


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


class getReviewSerializer(serializers.ModelSerializer):
    images = getImageSerializer(many=True, required=False)

    class Meta:
        model = Reviews
        fields = [
            'id', 'marker', 'financial_rating', 'avg_cost', 'covid_rating', 'care_rating', 'oxygen_rating',
            'beds_available',
            'ventilator_availability', 'oxygen_availability', 'icu_availability', 'comment', 'written_by', 'images'
        ]


class getSusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspiciousMarking
        fields = [
            'id', 'marker', 'comment', 'created_by_id', 'datef'
        ]
