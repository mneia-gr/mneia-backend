from typing import Dict, Optional

import rest_framework
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from isbnlib import is_isbn10, is_isbn13

from mneia_backend.models import abstract
from mneia_backend.models.link_type import LinkType
from mneia_backend.models.links.book_person import LinkBookPerson
from mneia_backend.utils import prettify_date


def validate_isbn(value) -> None:
    if value is None:
        return
    if len(value) not in [10, 13]:
        raise ValidationError(
            "Value %(value)s is neither 10 nor 13 digits long, got %(length)i digits.",
            params={"value": value, "length": len(value)},
        )
    if len(value) == 10 and not is_isbn10(value):
        raise ValidationError(f"Value {value} is not valid ISBN10.")
    if len(value) == 13 and not is_isbn13(value):
        raise ValidationError(f"Value {value} is not valid ISBN13.")


class Book(abstract.Model):
    name = models.CharField(max_length=255)
    edition = models.CharField(max_length=255)
    format = models.ForeignKey("BookFormat", related_name="books", on_delete=models.PROTECT)
    isbn = models.CharField("ISBN", max_length=13, null=True, blank=True, validators=[validate_isbn])
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
    def publication_date(self) -> Optional[str]:
        return prettify_date(self.publication_date_year, self.publication_date_month, self.publication_date_day)

    @property
    def as_yaml(self) -> Dict:
        return {
            "name": self.name,
            "title": self.name,
            "edition": self.edition,
            "format": self.format.name,
            "isbn": self.isbn,
            "pages_number": self.pages_number,
            "publication_date": self.publication_date,
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

    @property
    def editors(self):
        """Returns the instances of Person that are the editors of this Book, if there are any."""
        link_type = LinkType.objects.filter(entity_type0="book", entity_type1="person", name="editor").first()
        links_book_person = LinkBookPerson.objects.filter(book=self)
        links_book_person = [
            link_book_person for link_book_person in links_book_person if link_book_person.link.link_type == link_type
        ]
        return [link_book_person.person for link_book_person in links_book_person]

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
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
    list_display = ["name", "edition", "format", "isbn", "pages_number", "publication_date", "area"]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia"]
