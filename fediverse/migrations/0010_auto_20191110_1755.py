# Generated by Django 2.2.6 on 2019-11-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0009_follow_is_pending'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='fediID',
            field=models.URLField(blank=True, max_length=256, null=True, unique=True),
        ),
    ]
