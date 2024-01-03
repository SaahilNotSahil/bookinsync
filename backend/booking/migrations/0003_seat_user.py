# Generated by Django 5.0.1 on 2024-01-03 12:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_city_alter_route_dst_alter_route_src'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats', related_query_name='seat', to=settings.AUTH_USER_MODEL),
        ),
    ]
