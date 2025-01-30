from typing import Dict

import rest_framework
from babel.dates import format_date
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkMagazineIssuePhotograph(abstract.LinkModel):
    magazine_issue = models.ForeignKey("MagazineIssue", on_delete=models.PROTECT, related_name="links_to_photographs")
    photograph = models.ForeignKey("Photograph", on_delete=models.PROTECT, related_name="links_to_magazine_issues")
    link = models.ForeignKey(
        "Link",
        on_delete=models.PROTECT,
        limit_choices_to={"link_type__entity_type0": "magazine_issue", "link_type__entity_type1": "photograph"},
    )

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
            "photograph": {
                "id": str(self.photograph.id),
                "name": self.photograph.name,
            },
            "attributes": {},
        }

        # For each link attribute, add a key-value pair to the representation of this link as a reference.
        # TODO: Not all link attribute types have text values, need to figure this out later.
        link = self.link
        for link_attribute in link.link_attributes.all():
            link_attribute_type = link_attribute.attribute_type
            link_text_attribute_type = link_attribute_type.link_text_attribute_types.first()
            link_attribute_text_value = link_text_attribute_type.link_attribute_text_values.filter(link=link)[0]
            _["attributes"][link_attribute_type.name] = link_attribute_text_value.text_value

        return _

    class Meta:
        verbose_name = "Link Magazine Issue - Photograph"
        verbose_name_plural = "Links Magazine Issue - Photograph"


class LinkMagazineIssuePhotographSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkMagazineIssuePhotograph
        fields = "__all__"


class LinkMagazineIssuePhotographViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkMagazineIssuePhotograph.objects.all()
    serializer_class = LinkMagazineIssuePhotographSerializer


@admin.register(LinkMagazineIssuePhotograph)
class LinkMagazineIssuePhotographAdmin(admin.ModelAdmin):
    list_display = ["link", "magazine_issue", "photograph"]
    readonly_fields = ["id", "mbid", "edits_pending", "link_order", "entity0_credit", "entity1_credit"]
