from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy as _


class SportCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория вида спорта', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория Спорта")
        verbose_name_plural = _("Категории Спорта")


class Sport(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique = True)
    description = models.CharField(max_length=255, verbose_name='Описание')
    category = models.ForeignKey(SportCategory, on_delete=models.CASCADE, verbose_name='Категория спорта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Вид Спорта")
        verbose_name_plural = _("Виды Спорта")



class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    article = models.TextField(max_length=1000, verbose_name='Текст новости')
    author = models.ForeignKey('user.Editor', verbose_name="Автор", on_delete=models.CASCADE)
    photo = models.URLField(verbose_name='Фото')
    dateofadd = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')

    def __str__(self):
        return self.title

    
    class Meta:
        verbose_name = _("Новости")
        verbose_name_plural = _("Новости")
    
    

class Federation(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    admin = models.ForeignKey('user.Admin', on_delete=models.CASCADE, verbose_name='Админ Федерации')
    logo = models.URLField(verbose_name='Логотип')
    description = models.CharField(max_length=255, verbose_name='О нас')
    contacts = models.CharField(max_length=255, verbose_name='Контакты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Федерация Спорта")
        verbose_name_plural = _("Федерации Спорта")


class PlayerCategory(models.Model):
    name = CharField(max_length=255, verbose_name='Категория Спортсмена', unique=True)


class Player(models.Model):
    name = models.CharField(max_length = 255, verbose_name='Имя')
    surname = models.CharField(max_length = 255, verbose_name='Фамилия')
    age = models.IntegerField(verbose_name='Возраст', default=18)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    trainer = models.ForeignKey('user.Trainer', on_delete=models.CASCADE, verbose_name='Тренер')
    sex = models.CharField(max_length=255, verbose_name='Пол', unique=True, default='Мужчина')
    weight = models.IntegerField(verbose_name='Весовая категория', default=60)
    playercategory = models.ForeignKey(PlayerCategory, on_delete=models.CASCADE, verbose_name='Категория спортсмена', default=1)
    photo = models.URLField(verbose_name='Фото')
    dateofadd = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = _("Спортсмен")
        verbose_name_plural = _("Спортсмены")


class Event(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    creator = models.ForeignKey('user.Admin', on_delete=models.CASCADE, verbose_name='Организатор')
    date = models.DateTimeField(verbose_name='Дата проведения')
    location = models.CharField(max_length=255, verbose_name='Место проведения')
    player = models.ManyToManyField(Player, verbose_name='Спортсмены')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    description = models.CharField(max_length=255, verbose_name='Описание')
    photo = models.URLField(verbose_name='Фото')
    result = models.CharField(max_length=255, verbose_name='Результат')
    # is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Соревнования")
        verbose_name_plural = _("Соревнования")


class Matches(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Первый Спортсмен', related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Второй Спортсмен', related_name='player2')
    date = models.DateTimeField(verbose_name='Дата проведения')
    player1_score = models.IntegerField(verbose_name='Счет первого спортсмена', default=0)
    player2_score = models.IntegerField(verbose_name='Счет второго спортсмена', default=0)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Победитель', related_name='winner')
    


    def __str__(self):
        return f'{self.player1} - {self.player2}'

    class Meta:
        verbose_name = _("Матч")
        verbose_name_plural = _("Матчи")
