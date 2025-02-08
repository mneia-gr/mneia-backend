from django.contrib import admin
from django.db import models
from rest_framework import serializers, viewsets

from mneia_backend.models import abstract


class BookFormat(abstract.TypeModel):
    """
    Related schema: https://schema.org/BookFormatType
    """

    greek_name = models.CharField("Greek Name", max_length=255, null=True, blank=True)

    class Meta(abstract.TypeModel.Meta):
        verbose_name = "Book Format"
        verbose_name_plural = "Book Formats"


class BookFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFormat
        fields = "__all__"


class BookFormatViewSet(viewsets.ModelViewSet):
    queryset = BookFormat.objects.all()
    serializer_class = BookFormatSerializer


@admin.register(BookFormat)
class BookFormatAdmin(admin.ModelAdmin):
    list_display = ["name", "greek_name", "description", "mbid", "parent", "child_order"]
    readonly_fields = ["id", "mbid", "created_in_mneia"]
