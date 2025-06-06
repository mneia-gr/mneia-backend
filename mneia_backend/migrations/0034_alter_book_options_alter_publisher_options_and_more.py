# Generated by Django 5.2.1 on 2025-05-15 19:35

import mneia_backend.models.book
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0033_person_reference_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"ordering": ["name"], "verbose_name": "Book", "verbose_name_plural": "Books"},
        ),
        migrations.AlterModelOptions(
            name="publisher",
            options={"ordering": ["name"], "verbose_name": "Publisher", "verbose_name_plural": "Publishers"},
        ),
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(
                blank=True,
                max_length=13,
                null=True,
                validators=[mneia_backend.models.book.validate_isbn],
                verbose_name="ISBN",
            ),
        ),
    ]
