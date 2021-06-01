from django.db.models.manager import Manager
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status, generics
from .models import *
from .serializers import *



class NewsAPIView(APIView):
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetail(APIView):
    def get(self, request, pk, format=None):
        news = News.objects.get(pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        news = News.objects.get(pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        news = News.objects.get(pk=pk)
        serializer = serializers.NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SportsAPIView(APIView):
    def get(self, request):
        sport = Sport.objects.all()
        serializer = SportSerializer(sport, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SportsDetail(APIView):
    def get(self, request, pk, format=None):
        sport = Sport.objects.get(pk=pk)
        serializer = SportSerializer(sport)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        sport = Sport.objects.get(pk=pk)
        sport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        sport = Sport.objects.get(pk=pk)
        serializer = serializers.SportSerializer(sport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FederationsAPIView(APIView):
    def get(self, request):
        federation = Federation.objects.all()
        serializer = FederationSerializer(federation, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FederationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FederationsDetail(APIView):
    def get(self, request, pk, format=None):
        federation = Federation.objects.get(pk=pk)
        serializer = FederationSerializer(federation)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        federation = Federation.objects.get(pk=pk)
        federation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        federation = Federation.objects.get(pk=pk)
        serializer = serializers.FederationSerializer(federation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersAPIView(APIView):
    def get(self, request):
        player = Player.objects.all()
        serializer = PlayerSerializer(player, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersDetail(APIView):
    def get(self, request, pk, format=None):
        player = Player.objects.get(pk=pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        player = Player.objects.get(pk=pk)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        player = Player.objects.get(pk=pk)
        serializer = serializers.PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventsAPIView(APIView):
    def get(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventsDetail(APIView):
    def get(self, request, pk, format=None):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        event = Event.objects.get(pk=pk)
        serializer = serializers.EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchesAPIView(APIView):
    def get(self, request):
        matches = Matches.objects.all()
        serializer = MatchesSerializer(matches, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MatchesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchesDetail(APIView):
    def get(self, request, pk, format=None):
        matches = Matches.objects.get(pk=pk)
        serializer = MatchesSerializer(matches)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        matches = Matches.objects.get(pk=pk)
        matches.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        matches = Matches.objects.get(pk=pk)
        serializer = serializers.MatchesSerializer(matches, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)