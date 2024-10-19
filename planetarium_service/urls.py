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
router.register("astronomies", AstronomyShowViewSet)
router.register("reservations", ReservationViewSet)
router.register("tickets", TicketViewSet)
router.register("show_sessions", ShowSessionViewSet)
router.register("show_themes", ShowThemeViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium_service"
