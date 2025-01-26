from django.db import models

from mneia_backend.models import abstract


class LinkTextAttributeType(abstract.Model):
    attribute_type = models.ForeignKey("LinkAttributeType", on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Link Text Attribute Types"
        constraints = [models.UniqueConstraint(fields=["attribute_type"], name="unique")]
