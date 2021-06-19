import os
from configparser import RawConfigParser

from .base import *  # noqa

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_DIR = os.path.join(BASE_DIR, "../../config/")

parser = RawConfigParser()
parser.read_file(open(os.path.join(CONFIG_DIR, "app.ini")))

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": parser.get("database", "name"),
        "USER": parser.get("database", "user"),
        "PASSWORD": parser.get("database", "password"),
        "HOST": parser.get("database", "host") or "127.0.0.1",
        "PORT": parser.getint("database", "port") or "5432",
        "TEST": {
            "NAME": parser.get("test_database", "name"),
            "USER": parser.get("test_database", "user"),
            "PASSWORD": parser.get("test_database", "password"),
            "HOST": parser.get("test_database", "host") or "127.0.0.1",
            "PORT": parser.getint("test_database", "port") or "5432",
        },
    },
}

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = False

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = parser.get("app", "hosts").split(",")
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = parser.get("app", "secret")

# HAYSTACK CONFIGS
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "STATS_FILE": os.path.join(BASE_DIR, CONFIG_DIR, "webpack-stats-production.json"),
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "ERROR",
    },
}

# WEATHER API CONFIG
WEATHER_API = parser.get("weather_api", "api")
WEATHER_API_KEY = parser.get("weather_api", "key")
WEATHER_API_CURRENT_ENDPOINT = parser.get("weather_api", "current_weather_endpoint")
WEATHER_API_FORECAST_ENDPOINT = parser.get("weather_api", "forecast_weather_endpoint")
WEATHER_API_DEFAULT_ENDPOINT = WEATHER_API_FORECAST_ENDPOINT
WEATHER_API_MIN_FORECAST_DAYS = parser.getint("weather_api", "min_days")
WEATHER_API_MAX_FORECAST_DAYS = parser.getint("weather_api", "max_days")
