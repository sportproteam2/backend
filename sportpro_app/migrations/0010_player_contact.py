# Generated by Django 3.2.3 on 2021-07-28 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportpro_app', '0009_player_middlename'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='contact',
            field=models.CharField(default=' ', max_length=255, verbose_name='Контакты'),
        ),
    ]