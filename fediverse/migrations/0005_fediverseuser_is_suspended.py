# Generated by Django 2.2.6 on 2019-11-05 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0004_auto_20191105_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='fediverseuser',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
    ]
