# Generated by Django 2.2.6 on 2019-10-16 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0004_auto_20191016_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-posted',)},
        ),
    ]
