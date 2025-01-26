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

    magazine = models.ForeignKey("Magazine", on_delete=models.PROTECT)
    issue_number = models.CharField(max_length=15)
    order = models.PositiveSmallIntegerField()
    date_published = models.DateField()

    def __str__(self) -> str:
        return f"{self.magazine.name} - Issue {self.issue_number}"

    class Meta:
        verbose_name_plural = "Magazine Issues"
