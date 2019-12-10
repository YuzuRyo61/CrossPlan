# Generated by Django 2.2.6 on 2019-11-05 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fediverse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fromFediUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blocking', to='fediverse.FediverseUser')),
                ('fromUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blocking', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blocked', to=settings.AUTH_USER_MODEL)),
                ('targetFedi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blocked', to='fediverse.FediverseUser')),
            ],
        ),
    ]
