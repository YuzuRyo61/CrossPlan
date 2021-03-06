# Generated by Django 2.2.6 on 2019-11-20 02:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0013_tombuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='半角英数字とアンダーバーのみ使用できます。', regex='^[a-zA-Z0-9_]+$')]),
        ),
    ]
