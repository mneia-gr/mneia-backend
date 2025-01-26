import rest_framework
from django.contrib import admin
from django.db import models

from mneia_backend.models import abstract


class LinkMagazineIssuePhotograph(abstract.LinkModel):
    magazine_issue = models.ForeignKey("MagazineIssue", on_delete=models.PROTECT)
    photograph = models.ForeignKey("Photograph", on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Links Magazine Issue - Photograph"


class LinkMagazineIssuePhotographSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkMagazineIssuePhotograph
        fields = "__all__"


class LinkMagazineIssuePhotographViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkMagazineIssuePhotograph.objects.all()
    serializer_class = LinkMagazineIssuePhotographSerializer


@admin.register(LinkMagazineIssuePhotograph)
class LinkMagazineIssuePhotographAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkMagazineIssuePhotograph._meta.fields]
    readonly_fields = ["id", "mbid", "edits_pending", "link_order", "entity0_credit", "entity1_credit"]
