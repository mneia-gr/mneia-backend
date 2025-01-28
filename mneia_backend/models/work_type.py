from django.contrib import admin
from django_musicbrainz_connector.models import WorkType as MusicBrainzWorkType
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mneia_backend.models import abstract


class WorkType(abstract.TypeModel):
    class Meta(abstract.TypeModel.Meta):
        verbose_name_plural = "Work Types"


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"


class WorkTypeViewSet(viewsets.ModelViewSet):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer

    @action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of WorkType from an instance of MusicBrainzWorkType. API path:

            /work-types/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzWorkType.objects.get(id=mbid)
        try:
            instance = WorkType.objects.get(mbid=mb_instance.id)  # for now, do nothing if the Work Type already exists
        except WorkType.DoesNotExist:
            instance = WorkType(
                id=mb_instance.gid,
                mbid=mb_instance.id,
                name=mb_instance.name,
                child_order=mb_instance.child_order,
                description=mb_instance.description,
            )
            if mb_instance.parent is not None:
                # this assumes that the parent Work Type already exists:
                instance.parent = WorkType.objects.get(mbid=mb_instance.parent.id)
            instance.save()

        return Response(WorkTypeSerializer(instance=instance).data)


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WorkType._meta.fields]

    # all fields are read-only in Admin, because all Work Types come from MusicBrainz:
    readonly_fields = [field.name for field in WorkType._meta.fields]
