from sportpro_app.services import MatchesService
from django.db.models.manager import Manager
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status, viewsets, generics
from .models import *
from sportpro_app.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import *



class NewsViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, EditorAccessPermission]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()
        sport_id = self.request.query_params.get('sport')
        if sport_id is not None:
            queryset = queryset.filter(sport=sport_id)
        return queryset


class EventCategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, EditorAccessPermission]
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer


class SportViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, CoachAccessPermission]
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

    def get_queryset(self):
        queryset = Sport.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id is not None:
            queryset = queryset.filter(category=category_id)
        return queryset


class FederationiewSet(viewsets.ModelViewSet):
    # permission_classes = [AllowAny, AdminAccessPermission]
    queryset = Federation.objects.all()
    serializer_class = FederationSerializer

    def get_queryset(self):
        queryset = Federation.objects.all()
        sport_id = self.request.query_params.get('sport')
        if sport_id is not None:
            queryset = queryset.filter(sport=sport_id)
        return queryset


class PlayersViewSet(viewsets.ModelViewSet):
    # permission_classes = [AllowAny, CoachAccessPermission]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sport', 'sex', 'weight', 'playercategory', 'name']

    # def get_queryset(self):
    #     org = self.request.query_params.get("organization") # название такое же как и в пути
    #     return super().get_queryset().filter(trainer__organization=org)

    def get_queryset(self):
        queryset = Player.objects.all()
        org = self.request.query_params.get("organization")
        if org is not None:
            queryset = queryset.filter(trainer__organization=org)
        return queryset


class EventViewSet(viewsets.ModelViewSet):
    # permission_classes = [AdminAccessPermission]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sport', 'players', 'eventcategory']

    # def get_queryset(self):
    #     queryset = Event.objects.all()
    #     sport_id = self.request.query_params.get('sport')
    #     if sport_id is not None:
    #         queryset = queryset.filter(sport=sport_id)
    #     return queryset


class GridViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Grid.objects.all()
    serializer_class = GridSerializer


class MatchesViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [AdminAccessPermission, JudgeAccessPermission]
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer

    def get_queryset(self):
        queryset = Matches.objects.all()
        event_id = self.request.query_params.get('event')
        if event_id is not None:
            queryset = queryset.filter(sport=event_id)
        return queryset


class SportCategoryViewSet(viewsets.ModelViewSet):
    queryset = SportCategory.objects.all()
    serializer_class = SportCategorySerializer


class RegisterPlayersView(generics.CreateAPIView):
    queryset = PlayerToEvent.objects.all()
    serializer_class = PlayerToEventSerializer


class SetScoreView(generics.UpdateAPIView):
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer

    def perform_update(self, serializer):
        serializer.save()
        MatchesService.post_save(self.kwargs.get("pk"))
        MatchesService.define_winner(self.kwargs.get("pk"))

class GalleryView(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['federation', 'tags']


class PlayerCategoryView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, EditorAccessPermission]
    queryset = PlayerCategory.objects.all()
    serializer_class = PlayersCategorySerializer