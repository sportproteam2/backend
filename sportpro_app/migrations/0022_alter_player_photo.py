# Generated by Django 3.2.3 on 2021-07-08 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportpro_app', '0021_playertoevent_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='photo',
            field=models.URLField(null=True, verbose_name='Фото'),
        ),
    ]