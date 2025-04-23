from typing import Dict

import rest_framework
from django.contrib import admin
from django.db import models
from mneia_isbn import ISBN

from mneia_backend.models import abstract


class LinkBookPublisher(abstract.LinkModel):
    book = models.ForeignKey("Book", on_delete=models.PROTECT, related_name="links_to_publishers")
    publisher = models.ForeignKey("Publisher", on_delete=models.PROTECT, related_name="links_to_books")
    link = models.ForeignKey(
        "Link",
        on_delete=models.PROTECT,
        limit_choices_to={"link_type__entity_type0": "book", "link_type__entity_type1": "publisher"},
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
    def as_link_to_publisher(self) -> Dict:
        return {
            "link_phrase": self.link.link_type.long_link_phrase,
            "publisher": {
                "id": str(self.publisher.id),
                "name": self.publisher.name,
            },
        }

    @property
    def as_reference(self) -> Dict:
        _ = {
            "book": {
                "id": str(self.book.id),
                "name": self.book.name,
                "authors": [],
                "editors": [],
                "edition": self.book.edition,
                "publication_date": self.book.publication_date,
                "isbn": None,
            },
            "publisher": {
                "id": str(self.publisher.id),
                "name": self.publisher.name,
            },
        }

        if self.book.area:  # not every book has a known publication area
            _["book"]["area"] = str(self.book.area)

        if self.book.isbn:  # not every book has an ISBN
            isbn = ISBN(self.book.isbn)
            _["book"]["isbn"] = {
                "hyphenated": isbn.hyphenated,
            }

        for author in self.book.authors:
            _["book"]["authors"].append(
                {
                    "id": str(author.id),
                    "name": author.reference_name,
                }
            )

        for editor in self.book.editors:
            _["book"]["editors"].append(
                {
                    "id": str(editor.id),
                    "name": editor.reference_name,
                }
            )

        return _

    class Meta:
        verbose_name = "Link Book - Publisher"
        verbose_name_plural = "Links Book - Publisher"


class LinkBookPublisherSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkBookPublisher
        fields = "__all__"


class LinkBookPublisherViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkBookPublisher.objects.all()
    serializer_class = LinkBookPublisherSerializer


@admin.register(LinkBookPublisher)
class LinkBookPublisherAdmin(admin.ModelAdmin):
    list_display = ["link", "book", "publisher"]
    readonly_fields = ["id", "mbid", "edits_pending", "link_order", "entity0_credit", "entity1_credit"]
