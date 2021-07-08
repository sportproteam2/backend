from django.db.models.query import QuerySet
from .models import Event, Grid, Player, PlayerCategory, Sport, Matches
from user.models import User
from django.db.models import Max
from faker import Faker
import random

Faker.seed(0)

f = Faker()
sport = Sport.objects.last()
coach = User.objects.filter(role__name="Coach").last()
judge = User.objects.filter(role__name="referee").last()


sex = {
    1: "male",
    2: "female"
}


class PlayerService:

    @staticmethod
    def seed_players(size: int):
        for n in range(size):
            pc = PlayerCategory.objects.get(name="Junior")
            player = Player.objects.create(
                name=f.first_name(),
                surname=f.last_name(),
                age=random.randint(20, 40),
                sport=sport,
                trainer=coach,
                sex=sex.get(random.randint(1, 2)),
                weight=random.randint(60, 90),
                playercategory=pc
            )
            if player:
                print(n, ": OK")


class EventService:
    model = Event

    def choose_and_remove(items):
        # pick an item index
        if items:
            index = random.randrange(len(items))
            return items.pop(index)
        # nothing left!
        return None

    @classmethod
    def distribute_players(cls, queryset: QuerySet[Event]) -> None:
        # TODO implement for loop
        event = queryset.get()
        players = list(event.players.values_list("id", flat=True))
        stage = f"1/{len(players)//2}"
        number = 1

        while players:

            first = Player.objects.get(id=cls.choose_and_remove(players))
            second = Player.objects.get(id=cls.choose_and_remove(players))
            match = Matches.objects.create(
                player1=first,
                player2=second,
                judge=judge
            )
            grid = Grid.objects.create(
                number=number,
                stage=stage,
                event=event,
                match=match
            )

            number += 1

    @classmethod
    def get_next_stage(cls, stage):
        players = cls.model.objects.filter(
            stage=stage).values_list("match__winner", flat=True)
        return f"1/{len(players) // 2}"

    @classmethod
    def create_next_match(cls, grid, another_grid):
        stage = cls.get_next_stage(grid.stage)  # 1/5
        max_number = cls.model.objects.filter(stage=stage).aggregate(
            max_number=Max("number")).get("max_number")
        raise Exception(max_number)
        first = grid.match.winner
        second = another_grid.match.winner
