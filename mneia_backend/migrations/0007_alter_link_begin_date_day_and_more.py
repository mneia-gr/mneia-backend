# Generated by Django 5.1.4 on 2025-01-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0006_alter_linktype_entity_type0_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="begin_date_day",
            field=models.SmallIntegerField(blank=True, null=True, verbose_name="Begin Date Day"),
        ),
        migrations.AlterField(
            model_name="link",
            name="begin_date_month",
            field=models.SmallIntegerField(blank=True, null=True, verbose_name="Begin Date Month"),
        ),
        migrations.AlterField(
            model_name="link",
            name="begin_date_year",
            field=models.SmallIntegerField(blank=True, null=True, verbose_name="Begin Date Year"),
        ),
        migrations.AlterField(
            model_name="link",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created"),
        ),
        migrations.AlterField(
            model_name="link",
            name="end_date_day",
            field=models.SmallIntegerField(blank=True, null=True, verbose_name="End Date Day"),
        ),
        migrations.AlterField(
            model_name="link",
            name="end_date_month",
            field=models.SmallIntegerField(blank=True, null=True, verbose_name="End Date Month"),
        ),
        migrations.AlterField(
            model_name="link",
            name="end_date_year",
            field=models.SmallIntegerField(blank=True, null=True, verbose_name="End Date Year"),
        ),
    ]
