from django.db.models import Count, F
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from planetarium_service.pagination import ReservationPagination
from planetarium_service.models import (
    PlanetariumDome,
    ShowSession,
    ShowTheme,
    AstronomyShow,
    Reservation,
    Ticket,
)
from planetarium_service.serializers import (
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ShowThemeSerializer,
    AstronomyShowSerializer,
    ReservationSerializer,
    TicketSerializer,
    PlanetariumDomeImageSerializer,
    PlanetariumDomeDetailSerializer,
    AstronomyShowListSerializer,
    ShowSessionListSerializer,
    TicketListSerializer,
    ReservationListSerializer
)


class PlanetariumDomeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeSerializer
        if self.action == "retrieve":
            return PlanetariumDomeDetailSerializer
        return PlanetariumDomeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowSessionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = (
        ShowSession.objects
        .select_related("astronomy_show", "planetarium_dome")
        .annotate(
            tickets_available=(
                F("planetarium_dome__rows")
                * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ShowSessionListSerializer
        return self.serializer_class


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AstronomyShowListSerializer
        return self.serializer_class


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return self.serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(reservation__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        reservation_id = self.request.data.get("reservation")
        reservation = get_object_or_404(Reservation, id=reservation_id)
        serializer.save(reservation=reservation)
