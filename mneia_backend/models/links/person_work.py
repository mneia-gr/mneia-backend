from typing import Dict

import rest_framework
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkPersonWork(abstract.LinkModel):
    person = models.ForeignKey("Person", on_delete=models.PROTECT, related_name="links_to_works")
    work = models.ForeignKey("Work", on_delete=models.PROTECT, related_name="links_to_people")

    @property
    def as_link_to_work(self) -> Dict:
        return {
            "link_phrase": self.link.link_type.long_link_phrase,
            "work": {
                "id": str(self.work.id),
                "name": self.work.name,
            },
        }

    @property
    def as_link_to_person(self) -> Dict:
        return {
            "link_phrase": self.link.link_type.reverse_link_phrase,
            "person": {
                "id": str(self.person.id),
                "name": self.person.name,
            },
        }

    class Meta:
        verbose_name_plural = "Links Person - Work"


class LinkPersonWorkSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkPersonWork
        fields = "__all__"


class LinkPersonWorkViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkPersonWork.objects.all()
    serializer_class = LinkPersonWorkSerializer


@admin.register(LinkPersonWork)
class LinkPersonWorkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkPersonWork._meta.fields]
    readonly_fields = ["id", "mbid", "edits_pending", "link_order", "entity0_credit", "entity1_credit"]
