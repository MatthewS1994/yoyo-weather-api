from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework.test import APIRequestFactory

from apps.weather.client import WeatherClient

from .models import City


class CityDatabaseTableTests(TestCase):
    """
    This test will get or create a city from the database Table `City`
    The list of valid Cities can be found from the below source:

        http://bulk.openweathermap.org/sample/city.list.json.gz

    - Download the database by running the below command:

        python src/manage.py import_cities [--remove]

    a sample record consists of the following data:

    >>> {
    >>>    "id": 3369157,
    >>>    "name": "Cape Town",
    >>>    "state": "",
    >>>    "country": "ZA",
    >>>    "coord": {
    >>>      "lon": 18.42322,
    >>>      "lat": -33.925838
    >>>    }
    >>> }

    """

    sample_city_record = {
        "related_id": 3369157,
        "title": "Cape Town",
        "country_code": "ZA",
        "lon": 18.42322,
        "lat": -33.925838,
    }
    sample_city_record_object = None

    def setUp(self) -> None:
        self.sample_city_record_object = self.test_get_or_create_city()

        self.assertIsNotNone(getattr(settings, "WEATHER_API", None))
        self.assertIsNotNone(getattr(settings, "WEATHER_API_KEY", None))
        self.assertIsNotNone(getattr(settings, "WEATHER_API_MAX_FORECAST_DAYS", None))

        self.max_days = getattr(settings, "WEATHER_API_MAX_FORECAST_DAYS")

        self.factory = WeatherClient(self.sample_city_record_object.title, days=self.max_days)
        self.api_factory = APIRequestFactory()
        self.django_factory = RequestFactory()

    def test_get_or_create_city(self):
        city_object, _ = City.objects.get_or_create(**self.sample_city_record)
        return city_object

    def test_get_api_client_data_default(self):
        call = self.factory.get_default()
        self.assertEqual(call.status_code, 200)

    def test_get_api_client_data_current(self):
        call = self.factory.get_current()
        self.assertEqual(call.status_code, 200)

    def test_get_api_client_data_forecast(self):
        call = self.factory.get_forecast()
        self.assertEqual(call.status_code, 200)

    def test_city_list_api_success_response(self):
        request = self.client.get("/api/city/", format="json")
        self.assertEqual(request.status_code, 200)

    def test_city_forecast_api(self):
        response = self.client.get(
            "/api/locations/%s/?days=%d"
            % (
                self.sample_city_record_object.title,
                self.max_days,
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_city_forecast_day_validation_error_api(self):
        days = self.max_days + 2
        response = self.client.get(
            "/api/locations/%s/?days=%d"
            % (
                self.sample_city_record_object.title,
                days,
            ),
            format="json",
        )
        self.assertNotEqual(response.status_code, 200)
