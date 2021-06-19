from django.urls import reverse
from rest_framework import serializers

from apps.weather.models import City


class CitySerializer(serializers.HyperlinkedModelSerializer):
    forecast_url = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = [
            "url",
            "title",
            "forecast_url",
        ]

    def get_forecast_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(reverse("city-forecast", args=(obj.title,)))


class ForecastSerializer(serializers.Serializer):
    maximum = serializers.FloatField()
    minimum = serializers.FloatField()
    average = serializers.FloatField()
    median = serializers.FloatField()

    class Meta:
        fields = [
            "maximum",
            "minimum",
            "average",
            "median",
        ]
