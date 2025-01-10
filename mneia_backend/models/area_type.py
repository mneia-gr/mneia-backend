from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models import AreaType as MusicBrainzAreaType
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mneia_backend.models import abstract


class AreaType(abstract.Model):
    mbid = models.IntegerField(
        "MBID",
        help_text="The MusicBrainz integer ID",
    )
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)
    child_order = models.IntegerField("Child Order")
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Area Types"
        ordering = ["name"]


class AreaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaType
        fields = "__all__"


class AreaTypeViewSet(viewsets.ModelViewSet):
    queryset = AreaType.objects.all()
    serializer_class = AreaTypeSerializer

    @action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of AreaType from an instance of MusicBrainzAreaType. API path:

            /area-types/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzAreaType.objects.get(id=mbid)
        try:
            instance = AreaType.objects.get(mbid=mb_instance.id)  # for now, do nothing if the Area Type already exists
        except AreaType.DoesNotExist:
            instance = AreaType(
                id=mb_instance.gid,
                mbid=mb_instance.id,
                name=mb_instance.name,
                child_order=mb_instance.child_order,
                description=mb_instance.description,
            )
            if mb_instance.parent is not None:
                # this assumes that the parent Area Type already exists:
                instance.parent = AreaType.objects.get(mbid=mb_instance.parent.id)
            instance.save()

        return Response(AreaTypeSerializer(instance=instance).data)


@admin.register(AreaType)
class AreaTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AreaType._meta.fields]

    # all fields are read-only in Admin, because all Area Types come from MusicBrainz:
    readonly_fields = [field.name for field in AreaType._meta.fields]
