# Generated by Django 3.1.4 on 2020-12-21 11:42

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blogg', '0007_auto_20201221_1141'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
    ]
