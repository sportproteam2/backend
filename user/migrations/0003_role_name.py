# Generated by Django 3.2.3 on 2021-05-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='name',
            field=models.IntegerField(choices=[(1, 'Editor'), (2, 'Admin'), (3, 'Trainer')], default=1),
        ),
    ]
