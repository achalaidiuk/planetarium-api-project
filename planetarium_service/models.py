from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row
    def __str__(self):
        return self.name


class ShowTheme(models.Model):
    name = models.CharField(max_length=63)
    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=63)
    description = models.ManyToManyField(ShowTheme)

    def __str__(self):
        return self.title


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(
        PlanetariumDome, on_delete=models.CASCADE
    )
    show_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.astronomy_show


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.created_at} - {self.user}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    def __str__(self):
        return (
            f"{str(self.show_session)} (row: {self.row}, seat: {self.seat})"
        )

    @staticmethod
    def validate_ticket(row, seat, show_session, error_to_raise):
        planetarium_dome = show_session.planetarium_dome
        for (ticket_attr_value, ticket_attr_name,
             planetarium_dome_attr_name) in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, planetarium_dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name:
                            f"{ticket_attr_name} "
                            f"number must be in available range: "
                            f"(1, {planetarium_dome_attr_name}): "
                            f"(1, {count_attrs})"
                    }
                )
