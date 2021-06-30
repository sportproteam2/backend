from django.db.models import query
from rest_framework import serializers
from .models import *
from user.models import *
from user.serializers import TrainerSerializer, UserSerializer


class SportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SportCategory
        fields = ['id', 'name']


class SportSerializer(serializers.ModelSerializer):

    category = SportCategorySerializer(many=False)

    class Meta:
        model = Sport
        fields = ['id', 'name', 'description', 'category']

    def create(self, validated_data):
        category = validated_data.pop('category')
        obj, _ = SportCategory.objects.get_or_create(name=category.get('name'))
        validated_data["category"] = obj
        return super().create(validated_data)


class NewsSerializer(serializers.ModelSerializer):

    author = UserSerializer(many=False)
    sport = SportSerializer(many=False)

    class Meta:
        model = News
        fields = ['id', 'title', 'article', 'author', 'photo', 'dateofadd', 'sport']

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
    sport = SportSerializer(many = False)
    admin = UserSerializer(many = False)

    class Meta:
        model = Federation
        fields = ['id', 'name', 'sport', 'admin', 'logo', 'description', 'contacts']


class PlayersCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerCategory
        fields = ['id', 'name']


class PlayerSerializer(serializers.ModelSerializer):

    trainer = UserSerializer(many = False)
    sport = SportSerializer(many = False)
    playercategory = PlayersCategorySerializer(many = False)

    class Meta:
        model = Player
        fields = ['id', 'name', 'surname', 'age', 'sport', 'trainer', 'sex', 'weight', 'playercategory', 'photo', 'dateofadd']


    def create(self, validated_data):
        trainer = validated_data.pop('trainer')
        obj, _ = TrainerSerializer.objects.get_or_create(name=trainer.get('name'))
        validated_data["trainer"] = obj
        return super().create(validated_data)


class EventSerializer(serializers.ModelSerializer):

    sport = SportSerializer(many = False)
    creator = UserSerializer(many = False)

    class Meta:
        model = Event
        fields = ['id', 'name', 'creator', 'date', 'location', 'player', 'sport', 'description', 'photo', 'result']

    def create(self, validated_data):
        player_data = validated_data.pop('player')

        player = Player.objects.get_or_create(**player_data)
        event = Event.objects.create(player=player[0], **validated_data)

        for players in player_data:
            Player.objects.create(player=player, **players)

        return event


class MatchesSerializer(serializers.ModelSerializer):

    player1 = PlayerSerializer(many = False)
    player2 = PlayerSerializer(many = False)
    winner = PlayerSerializer(many = False)
    judge = UserSerializer(many = False)

    class Meta:
        model = Matches
        fields = ['id', 'player1', 'player2', 'date', 'player1_score', 'player2_score', 'winner', 'judge']
