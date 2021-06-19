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
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "TEST": {
            "NAME": os.path.join(BASE_DIR, "test-db.sqlite3"),
        },
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
