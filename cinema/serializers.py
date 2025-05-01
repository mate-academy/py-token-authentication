from django.db import transaction
from rest_framework import serializers

from cinema.models import (
    Genre,
    Actor,
    CinemaHall,
    Movie,
    MovieSession,
    Ticket,
    Order,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "title", "description", "duration", "genres", "actors")


class MovieListSerializer(MovieSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )


class MovieDetailSerializer(MovieSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ("id", "title", "description", "duration", "genres", "actors")


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")


class MovieSessionListSerializer(MovieSessionSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall_name = serializers.CharField(
        source="cinema_hall.name", read_only=True
    )
    movie_duration = serializers.IntegerField(
        source="movie.duration", read_only=True
    )
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity", read_only=True
    )

    class Meta:
        model = MovieSession
        fields = (
            "id",
            "show_time",
            "movie_title",
            "cinema_hall_name",
            "movie_duration",
            "cinema_hall_capacity",
        )


class MovieSessionDetailSerializer(MovieSessionSerializer):
    movie = MovieDetailSerializer(read_only=True)
    cinema_hall = CinemaHallSerializer(read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        """
        Validate ticket data using the static validate_ticket method from
        Ticket model. This method checks if row and seat numbers are
        within the cinema hall's capacity.
        """
        data = super(TicketSerializer, self).validate(attrs)
        row = attrs.get("row")
        seat = attrs.get("seat")
        movie_session = attrs.get("movie_session")

        if not all([row, seat, movie_session]):
            raise serializers.ValidationError(
                "Row, seat and movie_session are required"
            )

        # Using the static validate_ticket method from Ticket model
        # This method is defined in cinema/models.py
        Ticket.validate_ticket(
            row=row,
            seat=seat,
            cinema_hall=movie_session.cinema_hall,
            error_to_raise=serializers.ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "movie_session", "row", "seat")


class TicketListSerializer(TicketSerializer):
    movie_session = MovieSessionListSerializer(read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets", [])
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order

    def update(self, instance, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets", [])
            if tickets_data:
                instance.tickets.all().delete()
                for ticket_data in tickets_data:
                    Ticket.objects.create(order=instance, **ticket_data)
            return instance


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
