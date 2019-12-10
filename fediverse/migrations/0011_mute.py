# Generated by Django 2.2.6 on 2019-11-20 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0010_auto_20191110_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mute',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fromFediUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mute', to='fediverse.FediverseUser')),
                ('fromUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mute', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='muted', to=settings.AUTH_USER_MODEL)),
                ('targetFedi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='muted', to='fediverse.FediverseUser')),
            ],
        ),
    ]
