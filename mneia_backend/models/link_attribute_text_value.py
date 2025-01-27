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

    link = models.ForeignKey("Link", on_delete=models.PROTECT, related_name="link_attribute_text_values")
    attribute_type = models.ForeignKey(
        "LinkTextAttributeType",
        on_delete=models.PROTECT,
        related_name="link_attribute_text_values",
    )
    text_value = models.TextField()

    @property
    def link_explanation(self) -> str:
        """This is used in the Admin interface to help keep track of these values."""
        return self.link.explanation

    @property
    def attribute_type_name(self) -> str:
        """This is used in the Admin interface to help keep track of these values."""
        return self.attribute_type.attribute_type.name

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
    list_display = ["link_explanation", "attribute_type_name", "text_value"]
    readonly_fields = ["id", "link_explanation", "attribute_type_name"]
