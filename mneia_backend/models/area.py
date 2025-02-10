from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models import Area as MusicBrainzArea
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mneia_backend.models import abstract
from mneia_backend.models.area_type import AreaType


class Area(abstract.Model):
    mbid = models.IntegerField("MBID")
    name = models.CharField(max_length=255)
    type = models.ForeignKey("AreaType", on_delete=models.PROTECT, null=True)
    edits_pending = models.PositiveIntegerField("Edits Pending", default=0)
    last_updated = models.DateTimeField("Last Updated")
    begin_date_year = models.SmallIntegerField("Begin Date Year", null=True)
    begin_date_month = models.SmallIntegerField("Begin Date Month", null=True)
    begin_date_day = models.SmallIntegerField("Begin Date Day", null=True)
    end_date_year = models.SmallIntegerField("End Date Year", null=True)
    end_date_month = models.SmallIntegerField("End Date Month", null=True)
    end_date_day = models.SmallIntegerField("End Date Day", null=True)
    ended = models.BooleanField("Ended?", default=False)
    comment = models.CharField(max_length=255, default="")
    greek_name = models.CharField("Greek Name", max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.greek_name or self.name

    class Meta:
        verbose_name_plural = "Areas"
        ordering = ["name"]


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    @action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of Area from an instance of MusicBrainzArea. API path:

            /areas/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzArea.objects.get(id=mbid)
        try:
            instance = Area.objects.get(mbid=mb_instance.id)  # for now, do nothing if the Area already exists
        except Area.DoesNotExist:
            instance = Area(
                id=mb_instance.gid,
                mbid=mb_instance.id,
                name=mb_instance.name,
                edits_pending=mb_instance.edits_pending,
                last_updated=mb_instance.last_updated,
                begin_date_year=mb_instance.begin_date_year,
                begin_date_month=mb_instance.begin_date_month,
                begin_date_day=mb_instance.begin_date_day,
                end_date_year=mb_instance.end_date_year,
                end_date_month=mb_instance.end_date_month,
                end_date_day=mb_instance.end_date_day,
                ended=mb_instance.ended,
                comment=mb_instance.comment,
            )
            if mb_instance.type is not None:
                # this assumes that the Area Type already exists:
                instance.type = AreaType.objects.get(mbid=mb_instance.type.id)
            instance.save()

        return Response(AreaSerializer(instance=instance).data)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["name", "greek_name", "mbid", "type", "comment"]

    # All fields except 'greek_name' are read-only in Admin, because all Areas come from MusicBrainz:
    readonly_fields = [field.name for field in Area._meta.fields]
    readonly_fields.remove("greek_name")
