# Generated by Django 3.2.3 on 2021-05-31 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_role_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
