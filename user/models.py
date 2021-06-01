from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin) 
import jwt
from django.core.mail import send_mail



class UserManager(BaseUserManager):

    def create_user(self, username, name, surname, phone, email, role, password=None):

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if name is None or surname is None:
            raise TypeError('Users must have a name.')

        if phone is None:
            raise TypeError('Users must have a phone.')

        user = self.model(username=username, name=name, surname=surname, phone=phone, role=role, email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        return user

    def create_superuser(self, name, surname, username, password, phone, email, role):
 
        if password is None:
            raise TypeError('Superusers must have a password.')

        if username is None:
            raise TypeError('Superusers must have a username.')

        role_obj = Role.objects.get(id=role)

        user = self.create_user(username=username, email=email, password=password, phone=phone, role=role_obj, name=name, surname=surname)
        user.is_superuser = True
        user.save()

        return user


class Role(models.Model):

    CHOICES = [
        (1, 'Editor'),
        (2, 'Admin'),
        (3, 'Trainer'),]

    name = models.IntegerField(choices = CHOICES, default = 1)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Никнейм')
    email = models.EmailField(db_index=True, unique=True, verbose_name="Электронная почта")
    name = models.CharField(max_length = 255, verbose_name="Имя")
    surname = models.CharField(max_length = 255, verbose_name='Фамилия')
    role = models.ForeignKey(Role, on_delete = models.CASCADE, related_name='role', verbose_name="Роль")
    phone = models.CharField(max_length = 255, verbose_name='Номер телефона')
    is_active = models.BooleanField(default=True, verbose_name='Активный аккаунт')
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Отредактирован')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname', 'phone', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email

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


class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Редактор')


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Админ Федерации')
    FederationID = models.ForeignKey("sportpro_app.Federation", on_delete=models.CASCADE, verbose_name='Федерация')


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Тренер')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')