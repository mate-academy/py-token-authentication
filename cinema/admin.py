from django.contrib import admin

from .models import (
    CinemaHall,
    Genre,
    Actor,
    Movie,
    MovieSession,
    Order,
    Ticket,
)


class DisableDeleteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


@admin.register(CinemaHall)
class CinemaHallAdmin(DisableDeleteAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(DisableDeleteAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(DisableDeleteAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(DisableDeleteAdmin):
    pass


@admin.register(MovieSession)
class MovieSessionAdmin(DisableDeleteAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(DisableDeleteAdmin):
    pass


@admin.register(Order)
class OrderAdmin(DisableDeleteAdmin):
    pass
