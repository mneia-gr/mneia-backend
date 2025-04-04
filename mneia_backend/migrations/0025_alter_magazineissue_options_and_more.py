# Generated by Django 5.1.5 on 2025-02-02 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0024_worktype_greek_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="magazineissue",
            options={"ordering": ["order"], "verbose_name": "Magazine Issue", "verbose_name_plural": "Magazine Issues"},
        ),
        migrations.AddField(
            model_name="magazineissue",
            name="pages_number",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="The number of pages in this magazine issue",
                null=True,
                verbose_name="Pages Number",
            ),
        ),
        migrations.AlterField(
            model_name="worktype",
            name="greek_name",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Greek Name"),
        ),
    ]
