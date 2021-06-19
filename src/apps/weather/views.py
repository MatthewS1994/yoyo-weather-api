from dal import autocomplete
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from apps.weather.forms import CityForm
from apps.weather.models import City


class IndexView(TemplateView, FormView):
    form_class = CityForm
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        return ctx

    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("weather-index")
        context = super(IndexView, self).get_context_data(**kwargs)
        return self.render_to_response(context=context)


class CityAutocomplete(autocomplete.Select2QuerySetView):
    """
    Django Autocomplete Light:

    This view will return a list of filtered Cities from the database

    ?q=Cape Town
    """

    def get_queryset(self):
        qs = City.objects.all()
        if self.q:
            qs = qs.filter(Q(title__istartswith=self.q) | Q(country_code__istartswith=self.q))
        return qs
