from django.urls import path, include
from rest_framework import routers
from planetarium_service.views import (
    AstronomyShowViewSet,
    ReservationViewSet,
    TicketViewSet,
    ShowSessionViewSet,
    ShowThemeViewSet,
    PlanetariumDomeViewSet
)


router = routers.DefaultRouter()
router.register("astronomy", AstronomyShowViewSet)
router.register("reservation", ReservationViewSet)
router.register("tickets", TicketViewSet)
router.register("show_session", ShowSessionViewSet)
router.register("show_theme", ShowThemeViewSet)
router.register("planetarium_dome", PlanetariumDomeViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium_service"
