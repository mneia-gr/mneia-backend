from typing import Dict

from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class Magazine(abstract.Model):
    """
    Related schema: https://schema.org/Periodical
    """

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    @property
    def as_yaml(self) -> Dict:
        return {"name": self.name}


@admin.register(Magazine)
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Magazine._meta.fields]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia"]
