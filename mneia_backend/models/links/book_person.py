from typing import Dict

import rest_framework
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkBookPerson(abstract.LinkModel):
    book = models.ForeignKey("Book", on_delete=models.PROTECT, related_name="links_to_people")
    person = models.ForeignKey("Person", on_delete=models.PROTECT, related_name="links_to_books")
    link = models.ForeignKey(
        "Link",
        on_delete=models.PROTECT,
        limit_choices_to={"link_type__entity_type0": "book", "link_type__entity_type1": "person"},
    )

    @property
    def as_link_to_book(self) -> Dict:
        return {
            "link_phrase": self.link.link_type.reverse_link_phrase,
            "book": {
                "id": str(self.book.id),
                "name": self.book.name,
            },
        }

    @property
    def as_link_to_person(self) -> Dict:
        return {
            "link_phrase": self.link.link_type.long_link_phrase,
            "person": {
                "id": str(self.person.id),
                "name": self.person.name,
            },
        }

    class Meta:
        verbose_name = "Link Book - Person"
        verbose_name_plural = "Links Book - Person"


class LinkBookPersonSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkBookPerson
        fields = "__all__"


class LinkBookPersonViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkBookPerson.objects.all()
    serializer_class = LinkBookPersonSerializer


@admin.register(LinkBookPerson)
class LinkBookPersonAdmin(admin.ModelAdmin):
    list_display = ["link", "book", "person"]
    readonly_fields = ["id", "mbid", "edits_pending", "link_order", "entity0_credit", "entity1_credit"]
