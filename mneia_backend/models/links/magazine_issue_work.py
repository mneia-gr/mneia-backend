from typing import Dict

import rest_framework
from babel.dates import format_date
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkMagazineIssueWork(abstract.LinkModel):
    magazine_issue = models.ForeignKey("MagazineIssue", on_delete=models.PROTECT, related_name="links_to_works")
    work = models.ForeignKey("Work", on_delete=models.PROTECT, related_name="links_to_magazine_issues")

    @property
    def as_reference(self) -> Dict:
        _ = {
            "magazine": {
                "id": str(self.magazine_issue.magazine.id),
                "name": self.magazine_issue.magazine.name,
            },
            "magazine_issue": {
                "id": str(self.magazine_issue.id),
                "issue_number": self.magazine_issue.issue_number,
                "date_published": format_date(self.magazine_issue.date_published, format="long", locale="el_GR"),
            },
            "work": {"id": str(self.work.id), "name": self.work.name, "type": self.work.type.name, "authors": []},
            "attributes": {},
        }

        for author in self.work.authors:
            _["work"]["authors"].append(
                {
                    "id": str(author.id),
                    "name": author.name,
                }
            )

        # For each link attribute, add a key-value pair to the representation of this link as a reference.
        # TODO: Not all link attribute types have text values, need to figure this out later.
        link = self.link
        link_attributes = link.link_attributes.all()
        for link_attribute in link_attributes:
            link_attribute_type = link_attribute.attribute_type
            link_text_attribute_type = link_attribute_type.link_text_attribute_types.first()
            link_attribute_text_value = link_text_attribute_type.link_attribute_text_values.filter(link=link)[0]
            _["attributes"][link_attribute_type.name] = link_attribute_text_value.text_value

        return _

    class Meta:
        verbose_name_plural = "Links Magazine Issue - Work"


class LinkMagazineIssueWorkSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkMagazineIssueWork
        fields = "__all__"


class LinkMagazineIssueWorkViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkMagazineIssueWork.objects.all()
    serializer_class = LinkMagazineIssueWorkSerializer


@admin.register(LinkMagazineIssueWork)
class LinkMagazineIssueWorkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkMagazineIssueWork._meta.fields]
    readonly_fields = ["id", "mbid", "edits_pending", "link_order", "entity0_credit", "entity1_credit"]
