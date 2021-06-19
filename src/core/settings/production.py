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
