from django.db.models import query
from rest_framework import serializers
from .models import *
from user.models import *



class SportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SportCategory
        fields = ['id', 'name']


class NewsSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(queryset = Editor.objects.all())
    sport = serializers.PrimaryKeyRelatedField(queryset = Sport.objects.all())

    class Meta:
        model = News
        fields = ['id', 'title', 'article', 'author', 'photo', 'dateofadd', 'sport']


class SportSerializer(serializers.ModelSerializer):

    category = SportCategorySerializer(many = False)

    class Meta:
        model = Sport
        fields = ['id', 'name', 'description', 'category']

    def create(self, validated_data):
        category = validated_data.pop('category')
        obj, _ = SportCategory.objects.get_or_create(name = category.get('name'))
        validated_data["category"] = obj
        return super().create(validated_data)



class FederationSerializer(serializers.ModelSerializer):

    # category = SportCategorySerializer(many = False)
    sport = serializers.PrimaryKeyRelatedField(queryset = Sport.objects.all())
    admin = serializers.PrimaryKeyRelatedField(queryset = Admin.objects.all())

    class Meta:
        model = Federation
        fields = ['id', 'name', 'sport', 'admin', 'logo', 'description', 'contacts']

    
class PlayerSerializer(serializers.ModelSerializer):

    trainer = serializers.PrimaryKeyRelatedField(queryset = Trainer.objects.all())
    sport = serializers.PrimaryKeyRelatedField(queryset = Sport.objects.all())

    class Meta:
        model = Player
        fields = ['id', 'name', 'surname', 'age', 'sport', 'trainer', 'photo', 'email', 'dateofadd']


class EventSerializer(serializers.ModelSerializer):

    sport = serializers.PrimaryKeyRelatedField(queryset = Sport.objects.all())
    player = serializers.PrimaryKeyRelatedField(queryset = Player.objects.all())
    creator = serializers.PrimaryKeyRelatedField(queryset = Admin.objects.all())

    class Meta:
        model = Event
        fields = ['id', 'name', 'creator', 'date', 'location', 'player', 'sport', 'description', 'photo', 'result']


class MatchesSerializer(serializers.ModelSerializer):

    player1 = serializers.PrimaryKeyRelatedField(queryset = Player.objects.all())
    player2 = serializers.PrimaryKeyRelatedField(queryset = Player.objects.all())
    winner = serializers.PrimaryKeyRelatedField(queryset = Player.objects.all())


    class Meta:
        model = Matches
        fields = ['id', 'player1', 'player2', 'date', 'score', 'winner']

