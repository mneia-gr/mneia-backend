from typing import Dict

import rest_framework
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkPersonPhotograph(abstract.LinkModel):
    person = models.ForeignKey("Person", on_delete=models.PROTECT, related_name="links_to_photographs")
    photograph = models.ForeignKey("Photograph", on_delete=models.PROTECT, related_name="links_to_people")

    @property
    def as_link_to_photograph(self) -> Dict:
        return {
            "link_phrase": self.link.link_type.long_link_phrase,
            "photograph": {
                "id": str(self.photograph.id),
                "name": self.photograph.name,
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
        verbose_name_plural = "Links Person - Photograph"


class LinkPersonPhotographSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkPersonPhotograph
        fields = "__all__"


class LinkPersonPhotographViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkPersonPhotograph.objects.all()
    serializer_class = LinkPersonPhotographSerializer


@admin.register(LinkPersonPhotograph)
class LinkPersonPhotographAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkPersonPhotograph._meta.fields]
    readonly_fields = ["id", "mbid", "edits_pending", "link_order", "entity0_credit", "entity1_credit"]
