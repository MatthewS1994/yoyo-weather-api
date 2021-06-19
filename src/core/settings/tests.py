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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "test-db.sqlite3"),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = parser.get("app", "secret")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ALLOWED_HOSTS

# HAYSTACK CONFIGS
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "STATS_FILE": os.path.join(BASE_DIR, CONFIG_DIR, "webpack-stats.json"),
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
    "loggers": {
        "weather": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
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
