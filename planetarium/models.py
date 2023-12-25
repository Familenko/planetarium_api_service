from django.contrib.auth import get_user_model
from django.db import models
from planetarium.utils import show_image_file_path


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to=show_image_file_path)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)
    astronomy_show = models.ManyToManyField(
        AstronomyShow, related_name="show_themes"
    )

    def __str__(self):
        return self.name


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} - {self.capacity}"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        "AstronomyShow",
        on_delete=models.CASCADE,
        related_name="show_sessions"
    )
    planetarium_dome = models.ForeignKey(
        "PlanetariumDome",
        on_delete=models.CASCADE,
        related_name="show_sessions"
    )
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["show_time"]

    def __str__(self):
        return (
            f"{self.astronomy_show} - "
            f"{self.planetarium_dome} - "
            f"{self.show_time}"
        )


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} - {self.created_at}"


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
        return f"{self.show_session} - {self.row} - {self.seat}"
