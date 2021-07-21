from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.utils.translation import ugettext_lazy as _


class SportCategory(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Категория вида спорта', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория Спорта")
        verbose_name_plural = _("Категории Спорта")


class Sport(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    description = models.CharField(max_length=255, verbose_name='Описание')
    category = models.ForeignKey(SportCategory, on_delete=models.CASCADE, verbose_name='Категория спорта')
    photo = models.URLField(verbose_name='Фото')
    short_desc = models.CharField(max_length=100, verbose_name='Краткое описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Вид Спорта")
        verbose_name_plural = _("Виды Спорта")


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    article = models.TextField(max_length=1000, verbose_name='Текст новости')
    author = models.ForeignKey(
        'user.User', verbose_name="Автор", on_delete=models.CASCADE)
    photo = models.URLField(verbose_name='Фото')
    dateofadd = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления')
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    tags = models.CharField(max_length=50, verbose_name='Тэги')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Новости")
        verbose_name_plural = _("Новости")


class Federation(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Название", unique=True)
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    admin = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, verbose_name='Админ Федерации')
    logo = models.URLField(verbose_name='Логотип')
    description = models.CharField(max_length=255, verbose_name='О нас')
    contacts = models.CharField(max_length=255, verbose_name='Контакты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Федерация Спорта")
        verbose_name_plural = _("Федерации Спорта")


class PlayerCategory(models.Model):
    name = CharField(
        max_length=255, verbose_name='Категория Спортсмена', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория Спортсмена")
        verbose_name_plural = _("Категории Спортсменов")


class Player(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    age = models.IntegerField(verbose_name='Возраст', default=18)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    trainer = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Тренер')
    sex = models.CharField(max_length=255, verbose_name='Пол')
    weight = models.IntegerField(verbose_name='Весовая категория', default=60)
    playercategory = models.ForeignKey(PlayerCategory, on_delete=models.CASCADE, verbose_name='Категория спортсмена', default=1)
    photo = models.URLField(verbose_name='Фото', null=True)
    dateofadd = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = _("Спортсмен")
        verbose_name_plural = _("Спортсмены")


class Event(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    creator = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, verbose_name='Организатор')
    date = models.DateTimeField(verbose_name='Дата проведения')
    location = models.CharField(
        max_length=255, verbose_name='Место проведения')
    players = models.ManyToManyField(
        Player, verbose_name='Спортсмены', through='PlayerToEvent')
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    description = models.CharField(max_length=255, verbose_name='Описание')
    photo = models.URLField(verbose_name='Фото')
    # result = models.CharField(max_length=255, verbose_name='Результат')

    # is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Соревнования")
        verbose_name_plural = _("Соревнования")


class Grid(models.Model):
    stage = models.CharField(_("Stage"), max_length=10)
    event = models.ForeignKey("sportpro_app.Event", verbose_name=_(
        "Event"), related_name="grids", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stage}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Сетка'
        verbose_name_plural = 'Сетки'


class Matches(models.Model):
    number = models.PositiveIntegerField(_("Number"))
    grid = models.ForeignKey("sportpro_app.Grid", verbose_name=_(
        "Сетка"), related_name="matches", on_delete=models.SET_NULL, null=True)
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE,
                                verbose_name='Первый Спортсмен', related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE,
                                verbose_name='Второй Спортсмен', related_name='player2')
    date = models.DateTimeField(verbose_name='Дата проведения', null=True)
    player1_score = models.IntegerField(
        verbose_name='Счет первого спортсмена', default=0)
    player2_score = models.IntegerField(
        verbose_name='Счет второго спортсмена', default=0)
    winner = models.ForeignKey(
        Player, on_delete=models.SET_NULL, verbose_name='Победитель', related_name='winner', null=True)
    judge = models.ForeignKey(
        'user.User', on_delete=models.SET_NULL, null=True, verbose_name='Судья')

    def __str__(self):
        return f'{self.player1} - {self.player2}'

    class Meta:
        verbose_name = _("Матч")
        verbose_name_plural = _("Матчи")


class PlayerToEvent(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, verbose_name='Спортсмен')
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name='Соревнование')
    is_approved = models.BooleanField("Is approved", default=False)
    final_score = models.PositiveSmallIntegerField(_("Итоговые очки"), default=0)


    def __str__(self):
        return self.player

    class Meta:
        verbose_name = _("Спортсмен на соревнования")
        verbose_name_plural = _("Спортсмены на соревнования")


class PhotoForGallery(models.Model):
    photo = models.URLField(verbose_name='Фотография')
    dateofadd = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = _("Фото для Галереи")
        verbose_name_plural = _("Фото для Галереи")



class Gallery(models.Model):
    federation = models.ForeignKey(Federation, on_delete=models.CASCADE, verbose_name='Федерация')
    tags = models.CharField(max_length=100, verbose_name='Тэги')
    photo = models.ManyToManyField(PhotoForGallery, verbose_name='Фотографии')

    def __str__(self):
        return f'Фотографии с {self.federation}'

    class Meta:
        verbose_name = _("Галерея")
        verbose_name_plural = _("Галереи")
