import requests
from django.conf import settings

WEATHER_API = getattr(settings, "WEATHER_API")
WEATHER_API_KEY = getattr(settings, "WEATHER_API_KEY")
WEATHER_API_CURRENT_ENDPOINT = getattr(settings, "WEATHER_API_CURRENT_ENDPOINT")
WEATHER_API_FORECAST_ENDPOINT = getattr(settings, "WEATHER_API_FORECAST_ENDPOINT")
WEATHER_API_DEFAULT_ENDPOINT = getattr(settings, "WEATHER_API_DEFAULT_ENDPOINT")
WEATHER_API_MIN_FORECAST_DAYS = getattr(settings, "WEATHER_API_MIN_FORECAST_DAYS")
WEATHER_API_MAX_FORECAST_DAYS = getattr(settings, "WEATHER_API_MAX_FORECAST_DAYS")


class WeatherClient(object):
    """
    Weather Client:
    One central place where the api will be constructed to prevent repetitive code.

    example usage:

        In [1]: from apps.weather.client import WeatherClient

        In [2]: from apps.weather.models import City

        In [3]: city = City.objects.get(title='Cape Town')

        In [4]: client = WeatherClient(city=city.title, days=2)

    """

    def __init__(self, city, days=1, params=None, serialize=False):
        self.endpoint = WEATHER_API
        self.api_key = WEATHER_API_KEY
        self.city = city
        self.days = days
        self.params = params
        self.serialize = serialize

        self.default_endpoint = f"{self.endpoint}{WEATHER_API_DEFAULT_ENDPOINT}"
        self.current_endpoint = f"{self.endpoint}{WEATHER_API_CURRENT_ENDPOINT}"
        self.forecast_endpoint = f"{self.endpoint}{WEATHER_API_FORECAST_ENDPOINT}"

    def get_default_params(self):
        """
        Put all the necessary values in a dict to create the query params to the api
        :return dict:
        """
        return dict(
            q=self.city,
            key=self.api_key,
            days=self.days,
            aqi="no",
            alerts="no",
        )

    def get_parameters(self):
        """
        Return any query params the user specifies
        :return dict:
        """
        return self.params if self.params else dict()

    def get(self, endpoint):
        """
        Useful function That does the request to the client

        All you need to do is parse the endpoint

        e.g. req = self.get(self.current_endpoint)

        e.g. req = self.get('/api/endpoint/')

        :param endpoint:
        :return Response:
        """
        params = {**self.get_default_params(), **self.get_parameters()}
        request = requests.get(endpoint, params=params)
        request.raise_for_status()
        return request

    def get_current(self):
        """
        Get the current Day weather data

        You can specify when creating the client instance by specifying `serialize=True` If you want just the JSON
        data to be parsed back to you. Otherwise the Response data will be returned

            client = WeatherClient(city=city.title, days=2, serialize=True)

        :return json or Response:
        """
        req = self.get(self.current_endpoint)
        return req.json() if self.serialize else req

    def get_forecast(self):
        """
        Get the Forecast weather data

        You can specify when creating the client instance by specifying `serialize=True` If you want just the JSON
        data to be parsed back to you. Otherwise the Response data will be returned

            client = WeatherClient(city=city.title, days=2, serialize=True)

        :return json or Response:
        """
        req = self.get(self.forecast_endpoint)
        return req.json() if self.serialize else req

    def get_default(self):
        req = self.get(self.default_endpoint)
        return req.json() if self.serialize else req
