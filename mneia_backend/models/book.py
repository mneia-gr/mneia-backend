from typing import Dict

import rest_framework
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


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
        }

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
