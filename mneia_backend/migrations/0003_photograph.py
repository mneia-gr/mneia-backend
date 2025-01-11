# Generated by Django 5.1.4 on 2025-01-11 14:00

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0002_area_gender_person"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photograph",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_in_mneia", models.DateTimeField(auto_now_add=True)),
                ("updated_in_mneia", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name_plural": "Photographs",
            },
        ),
    ]