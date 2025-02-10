from typing import Dict

import rest_framework
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract
from mneia_backend.models.link_type import LinkType
from mneia_backend.models.links.book_person import LinkBookPerson


class Book(abstract.Model):
    name = models.CharField(max_length=255)
    edition = models.CharField(max_length=255)
    format = models.ForeignKey("BookFormat", related_name="books", on_delete=models.PROTECT)
    isbn = models.CharField("ISBN", max_length=13, null=True, blank=True)
    pages_number = models.PositiveSmallIntegerField(
        "Pages Number", help_text="The number of pages in this book", null=True, blank=True
    )
    publication_date_year = models.SmallIntegerField("Publication Date Year", null=True, blank=True)
    publication_date_month = models.SmallIntegerField("Publication Date Month", null=True, blank=True)
    publication_date_day = models.SmallIntegerField("Publication Date Day", null=True, blank=True)
    area = models.ForeignKey("Area", null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name

    @property
    def as_yaml(self) -> Dict:
        return {
            "name": self.name,
            "title": self.name,
            "edition": self.edition,
            "format": self.format.name,
            "isbn": self.isbn,
            "pages_number": self.pages_number,
            "publication_date_year": self.publication_date_year,
            "links": {"people": [link_to_person.as_link_to_person for link_to_person in self.links_to_people.all()]},
            "references": {
                "publishers": [link_to_publisher.as_reference for link_to_publisher in self.links_to_publishers.all()],
            },
        }

    @property
    def authors(self):
        """Returns the instances of Person that are the authors of this Book, if there are any."""
        link_type = LinkType.objects.filter(entity_type0="book", entity_type1="person", name="author").first()
        links_book_person = LinkBookPerson.objects.filter(book=self)
        links_book_person = [
            link_book_person for link_book_person in links_book_person if link_book_person.link.link_type == link_type
        ]
        return [link_book_person.person for link_book_person in links_book_person]

    class Meta:
        ordering = ["name"]


class BookSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Book._meta.fields]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia"]
