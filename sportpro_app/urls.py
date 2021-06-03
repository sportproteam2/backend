from django.urls import path
from .views import *

app_name = 'sportpro_app'

urlpatterns = [
    path('api/news/', NewsAPIView.as_view()),
    path('api/news/<int:pk>', NewsDetail.as_view()),
    path('api/sport', SportsAPIView.as_view()),
    path('api/sport/<int:pk>', SportsDetail.as_view()),
    path('api/federations', FederationsAPIView.as_view()),
    path('api/federations/<int:pk>', FederationsDetail.as_view()),
    path('api/player', PlayersAPIView.as_view()),
    path('api/player/<int:pk>', PlayersDetail.as_view()),
    path('api/event', EventsAPIView.as_view()),
    path('api/event/<int:pk>', EventsDetail.as_view()),
    path('api/matches', MatchesAPIView.as_view()),
    path('api/matches/<int:pk>', MatchesDetail.as_view()),
    path('api/sportbycategories/<int:pk>/', SportBySportCategoryAPIView.as_view()),
    path('api/sportbyfederations/<int:pk>/', SportByFederationAPIView.as_view()),
    path('api/federationbycategories/<int:pk>', FederationBySportCategoryAPIView.as_view()),
    path('api/newsbysport/<int:pk>', NewsBySportAPIView.as_view()),
]

