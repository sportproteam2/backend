from rest_framework.fields import ReadOnlyField
from sportpro_app.services import PlayerService
from django.db.models import query
from rest_framework import serializers
from .models import *
from user.models import *
from user.serializers import UserSerializer

class SportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SportCategory
        fields = ['id', 'name']


class SportSerializer(serializers.ModelSerializer):

    category = SportCategorySerializer(many=False)

    class Meta:
        model = Sport
        fields = ['id', 'name', 'description', 'category', 'photo', 'short_desc']

    def create(self, validated_data):
        category = validated_data.pop('category')
        obj, _ = SportCategory.objects.get_or_create(name=category.get('name'))
        validated_data["category"] = obj
        return super().create(validated_data)


class NewsSerializer(serializers.ModelSerializer):

    author = UserSerializer(many=False)
    sport = SportSerializer(many=False)
    Judge = UserSerializer(many=False)

    class Meta:
        model = News
        fields = ['id', 'title', 'article', 'author', 'judge', 'photo', 'dateofadd', 'sport', 'tags']

    def create(self, validated_data):
        author = validated_data.pop('author')
        obj, _ = UserSerializer.objects.get_or_create(name=author.get('name'))
        validated_data["author"] = obj
        return super().create(validated_data)

    def create(self, validated_data):
        sport = validated_data.pop('sport')
        obj, _ = SportSerializer.objects.get_or_create(name=sport.get('name'))
        validated_data["sport"] = obj
        return super().create(validated_data)


class FederationSerializer(serializers.ModelSerializer):

    # category = SportCategorySerializer(many = False)
    sport = SportSerializer(many=False)
    admin = UserSerializer(many=False)

    class Meta:
        model = Federation
        fields = ['id', 'name', 'sport', 'admin',
                  'logo', 'description', 'contacts']


class PlayersCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerCategory
        fields = ['id', 'name']


class PlayerSerializer(serializers.ModelSerializer):

    trainer = UserSerializer(many=False)
    sport = SportSerializer(many=False)
    playercategory = PlayersCategorySerializer(many=False)
    score = serializers.SerializerMethodField("get_score")
    organization = serializers.ReadOnlyField(source="trainer.organization")

    class Meta:
        model = Player
        fields = ['id', 'name', 'surname', 'age', 'sport', 'trainer', 'organization', 'sex', 'weight', 'playercategory', 'photo', 'dateofadd', 'score']

    def create(self, validated_data):
        trainer = validated_data.pop('trainer')
        obj, _ = User.objects.get(id=trainer.get('id'))
        validated_data["trainer"] = obj
        return super().create(validated_data)

    def get_score(self, obj):
        return PlayerService.get_score(obj)


class EventSerializer(serializers.ModelSerializer):

    sport = SportSerializer(many=False)
    creator = UserSerializer(many=False)

    class Meta:
        model = Event
        fields = ['id', 'name', 'creator', 'date', 'location',
                  'sport', 'description', 'photo']

    def create(self, validated_data):
        player_data = validated_data.pop('player')

        player = Player.objects.get_or_create(**player_data)
        event = Event.objects.create(player=player[0], **validated_data)

        for players in player_data:
            Player.objects.create(player=player, **players)

        return event


class MatchesSerializer(serializers.ModelSerializer):

    player1 = PlayerSerializer(many=False)
    player2 = PlayerSerializer(many=False)
    winner = PlayerSerializer(many=False)
    judge = UserSerializer(many=False)

    class Meta:
        model = Matches
        fields = ['id', 'player1', 'player2', 'date',
                  'player1_score', 'player2_score', 'winner', 'judge']


class GridSerializer(serializers.ModelSerializer):
    # match = MatchesSerializer()

    class Meta:
        model = Grid
        fields = '__all__'


class SetScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Matches
        fields = ['id', 'player1_score', 'player2_score']


class PlayerToEventSerializer(serializers.ModelSerializer):
    players = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = PlayerToEvent
        fields = ['id', 'players', 'event']

    def create(self, validated_data):
        player_data = validated_data.pop('players')
        event = validated_data.get('event')

        for player_id in player_data:
            player = Player.objects.get(id=player_id)
            instance = PlayerToEvent.objects.create(event=event, player=player)
        return instance


class PhotoForGallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoForGallery
        fields = ['id', 'photo', 'dateofadd']


class GallerySerializer(serializers.ModelSerializer):
    photo = PhotoForGallerySerializer(many = True)
    federation = FederationSerializer(many = False)

    class Meta:
        model = Gallery
        fields = ['id', 'federation', 'tags', 'photo']