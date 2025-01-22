from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models import LinkAttributeType as MusicBrainzLinkAttributeType
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mneia_backend.models import abstract


class LinkAttributeType(abstract.Model):
    mbid = models.IntegerField("MBID", null=True)  # optional, because there are link attribute types specific to Mneia
    parent = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.PROTECT,
        related_name="child_link_attribute_types",
    )
    root = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="leaf_child_attribute_types",
    )
    child_order = models.IntegerField("Child Order", default=0)
    name = models.CharField(max_length=255)
    description = models.TextField(db_column="description", null=True)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Link Attribute Types"


class LinkAttributeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkAttributeType
        fields = "__all__"


class LinkAttributeTypeViewSet(viewsets.ModelViewSet):
    queryset = LinkAttributeType.objects.all()
    serializer_class = LinkAttributeTypeSerializer

    @action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of LinkAttributeType from an instance of MusicBrainzLinkType. API path:

            /link-attribute-types/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzLinkAttributeType.objects.get(id=mbid)
        try:
            instance = LinkAttributeType.objects.get(mbid=mb_instance.id)  # do nothing if the instance already exists
        except LinkAttributeType.DoesNotExist:
            instance = LinkAttributeType(
                id=mb_instance.gid,
                mbid=mb_instance.id,
                child_order=mb_instance.child_order,
                name=mb_instance.name,
                description=mb_instance.description,
                last_updated=mb_instance.last_updated,
            )
            if mb_instance.parent is not None:
                instance.parent = LinkAttributeType.objects.get(mbid=mb_instance.parent.id)
            if mb_instance.root.id == mb_instance.id:  # instance is its own root:
                instance.root_id = instance.id
            else:
                instance.root = LinkAttributeType.objects.get(mbid=mb_instance.root.id)
            instance.save()

        return Response(LinkAttributeTypeSerializer(instance=instance).data)


@admin.register(LinkAttributeType)
class LinkAttributeTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkAttributeType._meta.fields]

    readonly_fields = [
        "id",
        "mbid",
    ]
