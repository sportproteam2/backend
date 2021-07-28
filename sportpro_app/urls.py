from django.urls import path
from sportpro_app import views
from rest_framework import routers

app_name = 'sportpro_app'

router = routers.DefaultRouter()
router.register("api/news", views.NewsViewSet)
router.register("api/sport", views.SportViewSet)
router.register("api/federation", views.FederationiewSet)
router.register("api/players", views.PlayersViewSet)
router.register("api/playercategory", views.PlayerCategoryView)
router.register("api/event", views.EventViewSet)
router.register("api/matches", views.MatchesViewSet)
router.register("api/sportcategory", views.SportCategoryViewSet)
router.register("api/grids", views.GridViewSet)
router.register("api/gallery", views.GalleryView)
router.register("api/eventcategory", views.EventCategoryViewSet)


urlpatterns = [
    path('api/registerplayers', views.RegisterPlayersView.as_view()),
    path('api/matches/<int:pk>/set_score/', views.SetScoreView.as_view())
] + router.urls
