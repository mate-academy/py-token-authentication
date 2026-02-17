from django.contrib import admin
from .models import Actor, CinemaHall, Genre, Movie, MovieSession, Order

# Registrando os modelos que existem no models.py
admin.site.register(Actor)
admin.site.register(CinemaHall)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieSession)
admin.site.register(Order)
