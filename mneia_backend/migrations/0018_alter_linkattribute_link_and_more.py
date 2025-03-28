# Generated by Django 5.1.5 on 2025-01-27 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mneia_backend", "0017_alter_magazineissue_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="linkattribute",
            name="link",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="link_attributes", to="mneia_backend.link"
            ),
        ),
        migrations.AlterField(
            model_name="linkattributetextvalue",
            name="attribute_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="link_attribute_text_values",
                to="mneia_backend.linktextattributetype",
            ),
        ),
        migrations.AlterField(
            model_name="linkattributetextvalue",
            name="link",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="link_attribute_text_values",
                to="mneia_backend.link",
            ),
        ),
        migrations.AlterField(
            model_name="linkmagazineissuephotograph",
            name="magazine_issue",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_to_photographs",
                to="mneia_backend.magazineissue",
            ),
        ),
        migrations.AlterField(
            model_name="linkmagazineissuephotograph",
            name="photograph",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_to_magazine_issues",
                to="mneia_backend.photograph",
            ),
        ),
        migrations.AlterField(
            model_name="linktextattributetype",
            name="attribute_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="link_text_attribute_types",
                to="mneia_backend.linkattributetype",
                verbose_name="Attribute Type",
            ),
        ),
    ]
