# Generated by Django 5.1.5 on 2025-02-10 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0032_area_greek_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="reference_name",
            field=models.CharField(default="FIXME", max_length=255, verbose_name="Reference Name"),
            preserve_default=False,
        ),
    ]
