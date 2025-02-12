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
        _ = {
            "name": self.name,
            "title": self.name,
            "references": {
                "books": [link_to_book.as_reference for link_to_book in self.links_to_books.all()],
            },
        }

        return _

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
        ordering = ["name"]


@admin.register(Publisher)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["name"]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia"]
