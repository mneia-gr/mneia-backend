import rest_framework
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkPersonPhotograph(abstract.LinkModel):
    person = models.ForeignKey("Person", on_delete=models.PROTECT)
    photograph = models.ForeignKey("Photograph", on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Links Person-Photograph"


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
