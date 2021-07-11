from typing import Iterable, List, Match, final
from django.db.models.query import QuerySet
from .models import Event, Grid, Player, PlayerCategory, PlayerToEvent, Sport, Matches
from user.models import User
from django.db.models import Max, Sum
from faker import Faker
from itertools import zip_longest
from django.db import transaction
import random

Faker.seed(0)

f = Faker()
# sport = Sport.objects.last()
# coach = User.objects.filter(role__name="Coach").last()
# judge = User.objects.filter(role__name="referee").last()


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

    @staticmethod
    def get_score(obj: Player):
        return PlayerToEvent.objects.filter(player=obj).aggregate(score=Sum("final_score")).get("score")


class EventService:
    model = Event

    @staticmethod
    def choose_and_remove(items: List):
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

        grid = Grid.objects.create(
            stage=stage,
            event=event,
        )
        while players:

            first = Player.objects.get(id=cls.choose_and_remove(players))
            second = Player.objects.get(id=cls.choose_and_remove(players))
            Matches.objects.create(
                grid=grid,
                number=number,
                player1=first,
                player2=second,
                judge=judge
            )

            number += 1

    @classmethod
    def get_players_in_stage(cls, stage: str):
        return list(cls.model.objects.filter(
            grids__stage=stage).values_list("grids__matches__winner", flat=True))

    @classmethod
    def get_next_stage(cls, stage):
        players = cls.get_players_in_stage(stage)
        return f"1/{len(players) // 2}"

    @classmethod
    def create_next_match(cls, grid, another_grid):
        stage = cls.get_next_stage(grid.stage)  # 1/5
        max_number = cls.model.objects.filter(stage=stage).aggregate(
            max_number=Max("number")).get("max_number")
        raise Exception(max_number)
        first = grid.match.winner
        second = another_grid.match.winner

    @classmethod
    def generate_next_stage(cls, event_id: int):
        grid = Grid.objects.filter(event=event_id).first()
        next_stage = f"1/{int(grid.stage.split('/').pop()) // 2}"
        # sid = transaction.savepoint()
        if grid.stage == "1/1":
            cls.give_points_to_players(grid.matches.last())
            return
        new_grid = Grid.objects.create(stage=next_stage, event=grid.event)
        matches_numbers = list(grid.matches.values_list(
            "number", flat=True).order_by("number"))
        groupped_matches_numbers = MatchesService.grouper(matches_numbers)
        for number, matches in enumerate(groupped_matches_numbers, start=1):
            first, second = [Matches.objects.filter(grid=grid).get(
                number=num) for num in matches]

            Matches.objects.create(
                number=number,
                grid=new_grid,
                player1=first.winner,
                player2=second.winner,
                judge=first.judge
            )

    @classmethod
    def give_points_to_players(cls, final_match: Match):
        first = final_match.winner  # 5
        second = final_match.player1 if final_match.winner.id == final_match.player2.id else final_match.player2
        qs = PlayerToEvent.objects.filter(event=final_match.grid.event)
        qs.filter(player=first).update(final_score=5)
        qs.filter(player=second).update(final_score=3)
        qs.exclude(player__in=[first, second]).update(final_score=1)


class MatchesService:

    model = Matches

    @staticmethod
    def grouper(iterable, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * 2
        return zip_longest(*args, fillvalue=fillvalue)

    @classmethod
    def define_winner(cls, instance: Matches) -> None:
        if instance.player1_score > instance.player2_score:
            instance.winner = instance.player1
        elif instance.player2_score > instance.player1_score:
            instance.winner = instance.player2
        instance.save()

    @classmethod
    def post_save(cls, match_id: int):
        instance = cls.model.objects.get(id=match_id)
        cls.define_winner(instance=instance)

        current_stage = instance.grid.stage
        max_number = cls.model.objects.filter(
            grid__stage=current_stage).aggregate(max_number=Max("number")).get("max_number")
        if instance.number == max_number:
            EventService.generate_next_stage(instance.grid.event.id)

    @classmethod
    def generate_random_scores(cls):
        first = random.randint(1, 10)
        second = random.randint(1, 10)
        if first == second:
            return cls.generate_random_scores()
        return first, second

    @classmethod
    def random_score(cls, queryset: QuerySet[Matches]) -> None:
        for match in queryset:
            first, second = cls.generate_random_scores()
            match.player1_score = first
            match.player2_score = second
            cls.define_winner(match)
