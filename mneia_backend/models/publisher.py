from typing import Dict

from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class Publisher(abstract.Model):
    """
    Related schema: https://schema.org/Organization
    """

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    @property
    def as_yaml(self) -> Dict:
        _ = {"name": self.name, "title": self.name}
        return _

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"


@admin.register(Publisher)
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Publisher._meta.fields]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia"]
