from typing import Dict

from babel.dates import format_date
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class MagazineIssue(abstract.Model):
    """
    Related schema: https://schema.org/PublicationIssue

    * `magazine`, foreign key to Magazine
    * `issue_number`: text, because some issues may have non-numeric numbering, e.g. Roman numerals
    * `order`: number, specifies the order in case the `issue_number` is not sortable, e.g. with Roman numerals
    * `date_published`, a date
    """

    magazine = models.ForeignKey("Magazine", on_delete=models.PROTECT, related_name="issues")
    issue_number = models.CharField(max_length=15)
    order = models.PositiveSmallIntegerField()
    date_published = models.DateField()

    def __str__(self) -> str:
        return f"{self.magazine.name} - Issue {self.issue_number}"

    @property
    def as_yaml(self) -> Dict:
        return {
            "issue_number": self.issue_number,
            "date_published": format_date(self.date_published, format="long", locale="el_GR"),
            "magazine": {
                "id": str(self.magazine.id),
                "name": self.magazine.name,
            },
            "references": {
                "photographs": [
                    link_to_photograph.as_reference for link_to_photograph in self.links_to_photographs.all()
                ],
                "works": [link_to_work.as_reference for link_to_work in self.links_to_works.all()],
            },
        }

    class Meta:
        verbose_name_plural = "Magazine Issues"
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["magazine", "issue_number"], name="do_not_repeat_issue_numbers_for_the_same_magazine"
            )
        ]


@admin.register(MagazineIssue)
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MagazineIssue._meta.fields]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia"]
