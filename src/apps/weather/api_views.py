import statistics

import django_filters
from django.conf import settings
from requests import HTTPError
from rest_framework import generics, viewsets
from rest_framework.response import Response

from apps.weather.client import WeatherClient
from apps.weather.models import City
from apps.weather.serializers import CitySerializer, ForecastSerializer

WEATHER_API_MAX_FORECAST_DAYS = getattr(settings, "WEATHER_API_MAX_FORECAST_DAYS")
WEATHER_API_MIN_FORECAST_DAYS = getattr(settings, "WEATHER_API_MIN_FORECAST_DAYS")


class CityViewSet(viewsets.ModelViewSet):
    """
    City ViewSet:

    Returns a list of Valid correct spelled City names.
    This endpoint will return the correct URL for the forecast API

    You can also use this API to search by the City tile or Country Code
    """

    serializer_class = CitySerializer
    lookup_field = "pk"
    queryset = City.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["title", "country_code"]

    def get_object(self):
        qs = super(CityViewSet, self).get_object()
        return qs


class CityApiView(generics.GenericAPIView):
    """

    The City Forecast API

    This endpoint goes inline with `CityViewSet` when the user searches for a valid City title.

    If the correct City kwargs id parsed in the url, it will return a valid forecast from the weather client

    http://0.0.0.0:8000/api/localations/{city}/
    http://0.0.0.0:8000/api/localations/{city}/?days=
    http://0.0.0.0:8000/api/localations/{city}/?days=1
    http://0.0.0.0:8000/api/localations/{city}/?days=16 (Will return validation error)
    http://0.0.0.0:8000/api/localations/No City Here/?days=16 (Will return validation error)

    The returned data would look as follows:

        [
            {
                "maximum": 23.1,
                "minimum": 14.5,
                "average": 18.1,
                "median": 18.299999999999997
            }
        ]

    """

    serializer_class = ForecastSerializer

    def get_queryset(self):
        return None

    def get_days_filters(self):
        """
        If the url query_params contains `days` Then we will validate it and return
        the correct value.

        If No `days` are in the query_params then we will default it to the WEATHER_API_MIN_FORECAST_DAYS
        from the settings file

        :return: int
        """
        if "days" in self.request.query_params and self.request.query_params["days"] != "":
            days = self.request.query_params["days"]
            if not int(days) > WEATHER_API_MAX_FORECAST_DAYS:
                return int(days)
            raise ValueError(
                "The Maximum number of days to select is between %d and %d"
                % (WEATHER_API_MIN_FORECAST_DAYS, WEATHER_API_MAX_FORECAST_DAYS)
            )
        return WEATHER_API_MIN_FORECAST_DAYS

    def get(self, request, *args, **kwargs):
        # Get the city from the url kwargs
        city = kwargs.pop("city", False)

        if city:
            try:
                # Apply the validation for the url params
                days = self.get_days_filters()
                # Fetch the City from the table
                city_obj = City.objects.filter(title=city).first()

                # Start the Client Connection
                forecast = WeatherClient(city_obj.title, days=days, serialize=True).get_forecast()
                forecast_days = []

                for forecast_day in forecast["forecast"]["forecastday"]:
                    # Find the median between the hourly temperatures
                    median = sorted([d["temp_c"] for d in forecast_day["hour"]], key=float)

                    # Append the list for serialization
                    forecast_days.append(
                        {
                            "maximum": forecast_day["day"]["maxtemp_c"],
                            "minimum": forecast_day["day"]["mintemp_c"],
                            "average": forecast_day["day"]["avgtemp_c"],
                            "median": statistics.median(median),
                        }
                    )

                # Serialize the data from the WeatherClient
                data = self.serializer_class(
                    forecast_days,
                    context={"request": request},
                    many=True,
                )
                return Response(data.data, status=200)
            except (City.DoesNotExist, HTTPError, ValueError) as e:
                return Response({"detail": str(e)}, status=400)

        return Response({"detail": str("City is required!")}, status=400)
