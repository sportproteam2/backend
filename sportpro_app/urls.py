from django.urls import path
from sportpro_app import views
from rest_framework import routers

app_name = 'sportpro_app'

router = routers.DefaultRouter()
router.register("api/news", views.NewsViewSet)
router.register("api/sport", views.SportViewSet)
router.register("api/federation", views.FederationiewSet)
router.register("api/players", views.PlayersViewSet)
router.register("api/event", views.EventViewSet)
router.register("api/matches", views.MatchesViewSet)

urlpatterns = router.urls