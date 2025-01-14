from django.contrib import admin
from django.db import models
from rest_framework import serializers, viewsets

from mneia_backend.models import abstract


class Photograph(abstract.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Photographs"


class PhotographSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photograph
        fields = "__all__"


class PhotographViewSet(viewsets.ModelViewSet):
    queryset = Photograph.objects.all()
    serializer_class = PhotographSerializer


@admin.register(Photograph)
class PhotographAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Photograph._meta.fields]
    readonly_fields = ["id"]
