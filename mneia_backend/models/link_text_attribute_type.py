from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkTextAttributeType(abstract.Model):
    attribute_type = models.ForeignKey(
        "LinkAttributeType",
        verbose_name="Attribute Type",
        on_delete=models.PROTECT,
        related_name="link_text_attribute_types",
    )

    class Meta:
        verbose_name_plural = "Link Text Attribute Types"
        constraints = [models.UniqueConstraint(fields=["attribute_type"], name="unique")]


@admin.register(LinkTextAttributeType)
class LinkTextAttributeTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkTextAttributeType._meta.fields]
    readonly_fields = ["id"]
