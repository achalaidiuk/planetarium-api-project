from django.db import transaction
from rest_framework import serializers
from planetarium_service.models import (
    PlanetariumDome,
    AstronomyShow,
    ShowSession,
    ShowTheme,
    Reservation,
    Ticket
)


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "image", "capacity")
        read_only_fields = ("capacity",)


class PlanetariumDomeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "image")


class PlanetariumDomeDetailSerializer(PlanetariumDomeSerializer):
    pass


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = "__all__"


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes_names = serializers.SerializerMethodField()

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "themes_names")

    def get_themes_names(self, obj):
        return obj.themes.values_list("name", flat=True)


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(ShowSessionSerializer):
    planetarium_dome = serializers.CharField(source="planetarium_dome.name")
    astronomy_show = serializers.CharField(source="astronomy_show.title")

    class Meta:
        model = ShowSession
        fields = ("id", "planetarium_dome", "astronomy_show", "show_time")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class TicketSerializer(serializers.ModelSerializer):
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        row = data.get("row")
        seat = data.get("seat")
        show_session_id = data.get("show_session")

        if Ticket.objects.filter(
                row=row, seat=seat, show_session_id=show_session_id
        ).exists():
            raise serializers.ValidationError("This place is already taken.")

        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "show_session",
            "planetarium_dome",
            "reservation"
        )


class TicketListSerializer(TicketSerializer):
    show_session = serializers.CharField(
        source="show_session.astronomy_show.title"
    )
    reservation = serializers.CharField(source="reservation.user.username")

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "show_session",
            "planetarium_dome",
            "reservation"
        )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")

    def create(self, validated_data):
        reservation = Reservation(**validated_data)

        with transaction.atomic():
            reservation.save()

        return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ("id", "user", "tickets")

    def get_user(self, obj):
        return obj.user.username
