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
        return [theme.name for theme in obj.themes.all()]


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(ShowSessionSerializer):
    planetarium_dome = serializers.SerializerMethodField()
    astronomy_show = serializers.SerializerMethodField()

    class Meta:
        model = ShowSession
        fields = ("id", "planetarium_dome", "astronomy_show", "show_time")

    def get_astronomy_show(self, obj):
        return obj.astronomy_show.title

    def get_planetarium_dome(self, obj):
        return obj.planetarium_dome.name


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
    show_session = serializers.SerializerMethodField()
    reservation = serializers.SerializerMethodField()

    def get_show_session(self, obj):
        return obj.show_session.astronomy_show.title

    def get_reservation(self, obj):
        return obj.reservation.user.username


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
