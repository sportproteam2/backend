from django.db.models.manager import Manager
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status, viewsets, generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import *



# class NewsAPIView(APIView):
#     def get(self, request):
#         news = News.objects.all()
#         sport_id = request.query_params.get("sport_id", None)
#         if sport_id is not None:
#             news = news.filter(sport=sport_id)
#         serializer = NewsSerializer(news, many = True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = NewsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, EditorAccessPermission]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


# class NewsDetail(APIView):
#     def get(self, request, pk, format=None):
#         news = News.objects.get(pk=pk)
#         serializer = NewsSerializer(news)
#         return Response(serializer.data)

#     def delete(self, request, pk, format=None):
#         news = News.objects.get(pk=pk)
#         news.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, pk, format=None):
#         news = News.objects.get(pk=pk)
#         serializer = serializers.NewsSerializer(news, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SportsAPIView(APIView):
#     def get(self, request):
#         sport = Sport.objects.all()
#         category_id = request.query_params.get("category_id", None)
#         if category_id is not None:
#             sport = sport.filter(category=category_id)
#         serializer = SportSerializer(sport, many = True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = SportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SportsDetail(APIView):
#     def get(self, request, pk, format=None):
#         sport = Sport.objects.get(pk=pk)
#         serializer = SportSerializer(sport)
#         return Response(serializer.data)

#     def delete(self, request, pk, format=None):
#         sport = Sport.objects.get(pk=pk)
#         sport.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, pk, format=None):
#         sport = Sport.objects.get(pk=pk)
#         serializer = serializers.SportSerializer(sport, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SportViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, CoachAccessPermission]
    queryset = Sport.objects.all()
    serializer_class = SportSerializer


# class FederationsAPIView(APIView):
#     def get(self, request):
#         federation = Federation.objects.all()
#         serializer = FederationSerializer(federation, many = True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = FederationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FederationsDetail(APIView):
#     def get(self, request, pk, format=None):
#         federation = Federation.objects.get(pk=pk)
#         serializer = FederationSerializer(federation)
#         return Response(serializer.data)

#     def delete(self, request, pk, format=None):
#         federation = Federation.objects.get(pk=pk)
#         federation.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, pk, format=None):
#         federation = Federation.objects.get(pk=pk)
#         serializer = serializers.FederationSerializer(federation, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FederationiewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, AdminAccessPermission]
    queryset = Federation.objects.all()
    serializer_class = FederationSerializer


# class PlayersAPIView(APIView):
#     def get(self, request):
#         player = Player.objects.all()
#         sport_id = request.query_params.get("sport_id", None)
#         if sport_id is not None:
#             player = player.filter(sport=sport_id)
#         serializer = PlayerSerializer(player, many = True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PlayerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PlayersDetail(APIView):
#     def get(self, request, pk, format=None):
#         player = Player.objects.get(pk=pk)
#         serializer = PlayerSerializer(player)
#         return Response(serializer.data)

#     def delete(self, request, pk, format=None):
#         player = Player.objects.get(pk=pk)
#         player.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, pk, format=None):
#         player = Player.objects.get(pk=pk)
#         serializer = serializers.PlayerSerializer(player, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersViewSet(viewsets.ModelViewSet):
    permission_classes = [CoachAccessPermission]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# class EventsAPIView(APIView):
#     def get(self, request):
#         event = Event.objects.all()
#         sport_id = request.query_params.get("sport_id", None)
#         if sport_id is not None:
#             event = event.filter(sport=sport_id)
#         serializer = EventSerializer(event, many = True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class EventsDetail(APIView):
#     def get(self, request, pk, format=None):
#         event = Event.objects.get(pk=pk)
#         serializer = EventSerializer(event)
#         return Response(serializer.data)

#     def delete(self, request, pk, format=None):
#         event = Event.objects.get(pk=pk)
#         event.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, pk, format=None):
#         event = Event.objects.get(pk=pk)
#         serializer = serializers.EventSerializer(event, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminAccessPermission]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# class MatchesAPIView(APIView):
#     def get(self, request):
#         matches = Matches.objects.all()
#         serializer = MatchesSerializer(matches, many = True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = MatchesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MatchesDetail(APIView):
#     def get(self, request, pk, format=None):
#         matches = Matches.objects.get(pk=pk)
#         serializer = MatchesSerializer(matches)
#         return Response(serializer.data)

#     def delete(self, request, pk, format=None):
#         matches = Matches.objects.get(pk=pk)
#         matches.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, pk, format=None):
#         matches = Matches.objects.get(pk=pk)
#         serializer = serializers.MatchesSerializer(matches, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchesViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminAccessPermission, JudgeAccessPermission]
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer


class SportCategoryViewSet(viewsets.ModelViewSet):
    queryset = SportCategory.objects.all()
    serializer_class = SportCategorySerializer
