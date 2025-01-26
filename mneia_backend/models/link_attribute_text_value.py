from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkAttributeTextValue(abstract.Model):
    """
    PostgreSQL Definition
    ---------------------

    The :code:`link_attribute_text_value` table is defined in the MusicBrainz Server as:

    .. code-block:: sql

        CREATE TABLE link_attribute_text_value ( -- replicate
            link                INT NOT NULL, -- PK, references link.id
            attribute_type      INT NOT NULL, -- PK, references link_text_attribute_type.attribute_type
            text_value          TEXT NOT NULL
        );
    """

    link = models.ForeignKey("Link", on_delete=models.PROTECT)
    attribute_type = models.ForeignKey("LinkTextAttributeType", on_delete=models.PROTECT)
    text_value = models.TextField()

    class Meta:
        verbose_name_plural = "Link Attribute Text Values"
        constraints = [
            models.UniqueConstraint(
                fields=["link", "attribute_type"],
                name="link_and_attribute_type_are_unique_together",
            )
        ]


@admin.register(LinkAttributeTextValue)
class LinkAttributeTextValueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkAttributeTextValue._meta.fields]
    readonly_fields = ["id"]
