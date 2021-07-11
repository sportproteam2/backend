# Generated by Django 3.2.3 on 2021-07-09 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sportpro_app', '0025_grid_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='matches',
        ),
        migrations.RemoveField(
            model_name='grid',
            name='match',
        ),
        migrations.RemoveField(
            model_name='grid',
            name='number',
        ),
        migrations.AddField(
            model_name='matches',
            name='grid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches', to='sportpro_app.grid', verbose_name='Сетка'),
        ),
        migrations.AddField(
            model_name='matches',
            name='number',
            field=models.PositiveIntegerField(default=0, verbose_name='Number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grid',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grids', to='sportpro_app.event', verbose_name='Event'),
        ),
    ]