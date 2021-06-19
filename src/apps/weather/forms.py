from dal import autocomplete
from django import forms

from apps.weather.models import City


class CityForm(forms.Form):
    days = forms.IntegerField()
    title = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url="city-autocomplete"),
    )

    class Meta:
        fields = ["title", "days"]
