# Generated by Django 5.1.4 on 2025-01-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0008_alter_area_mbid_alter_person_begin_area_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="mbid",
            field=models.IntegerField(blank=True, null=True, verbose_name="MBID"),
        ),
    ]