# Generated by Django 2.2.6 on 2019-10-16 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0005_auto_20191016_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, unique=True),
        ),
    ]