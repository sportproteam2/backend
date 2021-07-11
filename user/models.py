from datetime import datetime, timedelta
from sportpro_app.models import Sport
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db.models.fields.related import OneToOneField 
import jwt
from django.utils.translation import ugettext_lazy as _



class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, phone, password):
        """Create and return a `User` with an email, username and password."""

        if phone is None:
            raise TypeError('Users must have a phone.')

        user = self.model(phone=phone)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        
        user = self.create_user(phone=phone, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Role(models.Model):

    name = models.CharField(max_length=255, verbose_name='Роль', unique = True)
    
    class Meta:
        verbose_name = _("Роль")
        verbose_name_plural = _("Роли")

    def __str__(self):
        return self.name


class Region(models.Model):
    
    name = models.CharField(max_length=255, verbose_name='Область')

    class Meta:
        verbose_name = _("Область")
        verbose_name_plural = _("Области")

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length = 255, verbose_name="Имя")
    surname = models.CharField(max_length = 255, verbose_name='Фамилия')
    middlename = models.CharField(max_length=255, verbose_name='Отчество')
    role = models.ForeignKey(Role, on_delete = models.SET_NULL, related_name='role', verbose_name="Роль", null=True)
    phone = models.CharField(max_length = 255, verbose_name='Номер телефона', unique=True)
    region = models.ForeignKey(Region, on_delete = models.SET_NULL, null=True, verbose_name='Область')
    sport = models.ForeignKey(Sport, on_delete = models.SET_NULL, null=True, verbose_name='Спорт')
    is_active = models.BooleanField(default=True, verbose_name='Активный аккаунт')
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    # def __str__(self):
    #     return self.name

    @property
    def token(self):
        return self._generate_jwt_token()


    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")


class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Редактор')

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = _("Редактор")
        verbose_name_plural = _("Редакторы")


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Админ Федерации')

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = _("Представитель Федерации")
        verbose_name_plural = _("Представители Федерации")


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Тренер')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')

    def __str__(self):
        return f'{self.user.name} {self.user.surname}'

    class Meta:
        verbose_name = _("Тренер")
        verbose_name_plural = _("Тренеры")


class Judge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Судья')
    experience = models.IntegerField(verbose_name='Опыт работы', default=3)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = _("Судья")
        verbose_name_plural = _("Судьи")