from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.fields import AutoSlugField
from common.models import IndexedTimeStampedModel


class City(IndexedTimeStampedModel):
    """
    The City Model contains all the names of Cities across the world -
    which is imported using a JSON file from:

        http://bulk.openweathermap.org/sample/city.list.json.gz

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

    To Import this file run

    """

    title = models.CharField(
        _("Title"),
        max_length=255,
        db_index=True,
    )
    slug = AutoSlugField(
        _("Slug"), max_length=128, unique=True, populate_from=["title", "related_id"]
    )
    related_id = models.BigIntegerField()
    country_code = models.CharField(max_length=3, db_index=True)
    lat = models.FloatField()
    lon = models.JSONField()

    class Meta:
        ordering = ("title", "country_code")

    def __str__(self):
        return f"{self.title}"
