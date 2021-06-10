from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
from django.utils.translation import ugettext_lazy as _


class SportCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория вида спорта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория Спорта")
        verbose_name_plural = _("Категории Спорта")


class Sport(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
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
    photo = models.ImageField(verbose_name='Фото')
    dateofadd = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')

    def __str__(self):
        return self.title

    
    class Meta:
        verbose_name = _("Новости")
        verbose_name_plural = _("Новости")
    
    

class Federation(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    admin = models.ForeignKey('user.Admin', on_delete=models.CASCADE, verbose_name='Админ Федерации')
    logo = models.ImageField(verbose_name='Логотип')
    description = models.CharField(max_length=255, verbose_name='О нас')
    contacts = models.CharField(max_length=255, verbose_name='Контакты')
    # category = models.ForeignKey(SportCategory, on_delete=models.CASCADE, verbose_name='Категория спорта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Федерация Спорта")
        verbose_name_plural = _("Федерации Спорта")


class Player(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    age = models.IntegerField(verbose_name='Возраст')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    trainer = models.ForeignKey('user.Trainer', on_delete=models.CASCADE, verbose_name='Тренер')
    photo = models.ImageField(verbose_name='Фото')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
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
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Спортсмены')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='Вид спорта')
    description = models.CharField(max_length=255, verbose_name='Описание')
    photo = models.ImageField(verbose_name='Фото')
    result = models.CharField(max_length=255, verbose_name='Результат')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Соревнования")
        verbose_name_plural = _("Соревнования")


class Matches(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Первый Спортсмен', related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Второй Спортсмен', related_name='player2')
    date = models.DateTimeField(verbose_name='Дата проведения')
    score = models.CharField(max_length=20, verbose_name='Счет')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Победитель', related_name='winner')


    def __str__(self):
        return f'{self.player1} - {self.player2}'

    class Meta:
        verbose_name = _("Матч")
        verbose_name_plural = _("Матчи")
