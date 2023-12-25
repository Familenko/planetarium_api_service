from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowSessionViewSet,
    PlanetariumDomeViewSet,
    AstronomyShowViewSet,
    ShowThemeViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("show_session", ShowSessionViewSet)
router.register("planetarium_dome", PlanetariumDomeViewSet)
router.register("astronomy_show", AstronomyShowViewSet)
router.register("show_theme", ShowThemeViewSet)
router.register("reservation", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
