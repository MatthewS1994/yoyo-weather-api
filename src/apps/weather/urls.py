from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from .api_views import CityApiView, CityViewSet
from .views import CityAutocomplete, IndexView

router = routers.DefaultRouter()

# Weather ViewSets
router.register("city", CityViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", IndexView.as_view(), name="weather-index"),
    path("api/", include(router.urls)),
    path("api/locations/<str:city>/", CityApiView.as_view(), name="city-forecast"),
    path("api/cities/", CityAutocomplete.as_view(), name="city-autocomplete"),
]
