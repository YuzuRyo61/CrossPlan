# Generated by Django 2.2.6 on 2019-10-16 06:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='posted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]