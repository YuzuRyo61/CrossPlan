# Generated by Django 2.2.6 on 2019-11-06 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0008_auto_20191106_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
    ]
