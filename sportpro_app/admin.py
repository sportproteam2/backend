from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect
from .services import EventService, PlayerService
from django.urls import path


admin.site.register(News)
admin.site.register(Sport)
admin.site.register(Federation)
admin.site.register(Matches)
admin.site.register(SportCategory)
admin.site.register(PlayerCategory)


def approve(modeladmin, request, queryset):
    queryset.update(is_approved=True)


def distribute_players(modeladmin, request, queryset):
    EventService.distribute_players(queryset)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    actions = [distribute_players]


@admin.register(PlayerToEvent)
class PlayerToEventAdmin(admin.ModelAdmin):
    list_display = ["id", "event", "player", "is_approved"]
    actions = [approve]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["id", "surname"]
    change_list_template = "admin/players.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('seed_players/', self.seed_players, name='seed_players')
        ]
        return urls + custom_urls

    urls = property(get_urls)

    def seed_players(self, request, obj):
        PlayerService.seed_players(20)
        # self.message_user(request, "Players were created")
        return HttpResponseRedirect("../")


@admin.register(Grid)
class GridAdmin(admin.ModelAdmin):
    list_display = ['id', 'stage', 'number', 'match']
