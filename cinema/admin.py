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


class NoDeleteAdminMixin:
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


class BaseNoDeleteAdmin(NoDeleteAdminMixin, admin.ModelAdmin):
    """Base admin class non-removable"""
    pass


admin.site.register(CinemaHall, BaseNoDeleteAdmin)
admin.site.register(Genre, BaseNoDeleteAdmin)
admin.site.register(Actor, BaseNoDeleteAdmin)
admin.site.register(Movie, BaseNoDeleteAdmin)
admin.site.register(MovieSession, BaseNoDeleteAdmin)
admin.site.register(Order, BaseNoDeleteAdmin)
admin.site.register(Ticket, BaseNoDeleteAdmin)
