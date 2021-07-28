# Generated by Django 3.2.3 on 2021-07-28 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sportpro_app', '0011_auto_20210728_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Категория')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='license',
            field=models.CharField(default=' ', max_length=255, verbose_name='Лицензия'),
        ),
        migrations.AddField(
            model_name='event',
            name='eventcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sportpro_app.eventcategory', verbose_name='Категория соревнований'),
        ),
    ]
