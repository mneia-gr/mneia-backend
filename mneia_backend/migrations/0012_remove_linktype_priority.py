# Generated by Django 5.1.5 on 2025-01-19 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0011_alter_linkpersonphotograph_entity0_credit_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="linktype",
            name="priority",
        ),
    ]
