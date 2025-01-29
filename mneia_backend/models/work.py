from typing import Dict

import rest_framework
from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models.work import Work as MusicBrainzWork

from mneia_backend.models import abstract
from mneia_backend.models.work_type import WorkType


class Work(abstract.Model):
    # MBID is optional because there are Works in Mneia that are not imported from MusicBrainz:
    mbid = models.IntegerField("MBID", null=True, blank=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey("WorkType", on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, default="", blank=True)
    edits_pending = models.PositiveIntegerField("Edits Pending", default=0)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)

    def __str__(self) -> str:
        return self.name

    @property
    def as_yaml(self) -> Dict:
        return {
            "name": self.name,
            "links": {"people": [link_to_person.as_link_to_person for link_to_person in self.links_to_people.all()]},
        }

    class Meta:
        ordering = ["name"]


class WorkSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class WorkViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    @rest_framework.decorators.action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of Work from an instance of MusicBrainzWork. API path:

            /works/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzWork.objects.get(id=mbid)
        try:
            instance = Work.objects.get(mbid=mb_instance.id)  # for now, do nothing if the Work already exists
        except Work.DoesNotExist:
            instance = Work(
                id=mb_instance.gid,
                mbid=mb_instance.id,
                name=mb_instance.name,
                edits_pending=mb_instance.edits_pending,
                last_updated=mb_instance.last_updated,
            )
            if mb_instance.type is not None:
                # this assumes that the Work Type already exists:
                instance.type = WorkType.objects.get(mbid=mb_instance.type.id)
            instance.save()

        return rest_framework.response.Response(WorkSerializer(instance=instance).data)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Work._meta.fields]
    readonly_fields = ["id", "created_in_mneia", "updated_in_mneia", "mbid", "edits_pending", "last_updated"]
