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


class NoDeleteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


for model in (CinemaHall, Genre, Actor, Movie, MovieSession, Order, Ticket):
    admin.site.register(model, NoDeleteAdmin)
