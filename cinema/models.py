from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    class Meta:
        ordering = ["-show_time"]

    def __str__(self) -> str:
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        unique_together = ("movie_session", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self) -> str:
        return (
            f"{self.movie_session} (row: {self.row}, seat: {self.seat})"
        )

    @staticmethod
    def validate_ticket(
        row: int, seat: int, cinema_hall: CinemaHall, error_to_raise
    ):
        """
        Validate that the row and seat are within the cinema hall bounds.

        Keep the same signature and behavior (used by clean/serializers).
        """
        for value, field_name, hall_field in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            max_value = getattr(cinema_hall, hall_field)
            if not (1 <= value <= max_value):
                raise error_to_raise(
                    {
                        field_name: (
                            f"{field_name} number must be in available range: "
                            f"(1, {hall_field}): (1, {max_value})"
                        )
                    }
                )

    def clean(self) -> None:
        self.validate_ticket(
            self.row,
            self.seat,
            self.movie_session.cinema_hall,
            ValidationError,
        )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: set[str] | None = None,
    ):
        self.full_clean()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
