from django.contrib import admin
from .models import *



admin.site.register(News)
admin.site.register(Sport)
admin.site.register(Federation)
admin.site.register(Player)
admin.site.register(Event)
admin.site.register(Matches)
admin.site.register(SportCategory)
admin.site.register(PlayerCategory)
# admin.site.register(PlayerToEvent)


def approve(modeladmin, request, queryset):
    queryset.update(is_approved=True)


@admin.register(PlayerToEvent)
class PlayerToEventAdmin(admin.ModelAdmin):
    list_display = ["id", "event", "player", "is_approved"]
    actions = [approve]

