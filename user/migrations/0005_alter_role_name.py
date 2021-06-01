# Generated by Django 3.2.3 on 2021-05-31 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_role_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.IntegerField(choices=[(1, 'Editor'), (2, 'Admin'), (3, 'Trainer')], default=1),
        ),
    ]
