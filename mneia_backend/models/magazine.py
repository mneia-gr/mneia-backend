from typing import Dict

from babel.dates import format_date
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
        _ = {"name": self.name, "title": self.name, "issues": []}
        for issue in self.issues.all():
            _["issues"].append(
                {
                    "id": str(issue.id),
                    "issue_number": issue.issue_number,
                    "date_published": format_date(issue.date_published, format="long", locale="el_GR"),
                    "pages_number": issue.pages_number,
                }
            )
        return _


@admin.register(Magazine)
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Magazine._meta.fields]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia"]
