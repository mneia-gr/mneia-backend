from django.contrib import admin
from django_musicbrainz_connector.models import Gender as MusicBrainzGender
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mneia_backend.models import abstract


class Gender(abstract.TypeModel):
    class Meta(abstract.TypeModel.Meta):
        verbose_name_plural = "Genders"


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

    @action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of Gender from an instance of MusicBrainzGender. API path:

            /genders/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzGender.objects.get(id=mbid)
        try:
            instance = Gender.objects.get(mbid=mb_instance.id)  # for now, do nothing if the Gender already exists
        except Gender.DoesNotExist:
            instance = Gender(
                id=mb_instance.gid,
                mbid=mb_instance.id,
                name=mb_instance.name,
                child_order=mb_instance.child_order,
                description=mb_instance.description,
            )
            if mb_instance.parent is not None:
                # this assumes that the parent Gender already exists:
                instance.parent = Gender.objects.get(mbid=mb_instance.parent.id)
            instance.save()

        return Response(GenderSerializer(instance=instance).data)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Gender._meta.fields]

    # all fields are read-only in Admin, because all Genders come from MusicBrainz:
    readonly_fields = [field.name for field in Gender._meta.fields]
