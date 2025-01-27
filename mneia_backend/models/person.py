from typing import Dict

from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models import Artist as MusicBrainzArtist
from django_musicbrainz_connector.models import ArtistType as MusicBrainzArtistType
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mneia_backend.models import abstract
from mneia_backend.models.area import Area
from mneia_backend.models.gender import Gender


class Person(abstract.Model):
    """
    MusicBrainz structure:

    ```
    Artist
    |
    +--> Artist Type (e.g. "Person")
    |
    +--> Gender
    |
    +--> Area --> Area Type
    ```

    Mneia structure:

    ```
    Person
    |
    +--> Gender
    |
    +--> Area --> Area Type
    ```
    """

    # MBID is optional because there are people in Mneia that are not imported from MusicBrainz:
    mbid = models.IntegerField("MBID", null=True, blank=True)
    name = models.CharField(max_length=255)
    sort_name = models.CharField("Sort Name", max_length=255)
    begin_date_year = models.SmallIntegerField("Begin Date Year", null=True, blank=True)
    begin_date_month = models.SmallIntegerField("Begin Date Month", null=True, blank=True)
    begin_date_day = models.SmallIntegerField("Begin Date Day", null=True, blank=True)
    end_date_year = models.SmallIntegerField("End Date Year", null=True, blank=True)
    end_date_month = models.SmallIntegerField("End Date Month", null=True, blank=True)
    end_date_day = models.SmallIntegerField("End Date Day", null=True, blank=True)
    area = models.ForeignKey("Area", null=True, on_delete=models.PROTECT)
    gender = models.ForeignKey("Gender", null=True, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, default="", blank=True)
    edits_pending = models.PositiveIntegerField("Edits Pending", default=0)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    ended = models.BooleanField("Ended?", default=False)
    begin_area = models.ForeignKey(
        "Area",
        verbose_name="Begin Area",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="people_begin_area",
    )
    end_area = models.ForeignKey(
        "Area",
        verbose_name="End Area",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="people_end_area",
    )

    def __str__(self) -> str:
        return self.name

    @property
    def as_yaml(self) -> Dict:
        return {
            "name": self.name,
            "links": {
                "photographs": [
                    link_to_photograph.as_link_to_photograph for link_to_photograph in self.links_to_photographs.all()
                ]
            },
        }

    class Meta:
        verbose_name_plural = "People"
        ordering = ["name"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of Person from an instance of MusicBrainzArtist. Artists in MusicBraizn
        can be of different types, and "Person" is an Artist Type in MusicBrainz. Here, we have a separate model for
        Person. The MusicBrainz Artist Type is checked during the import, and an "HTTP 422 Unprocessable Entity" is
        returned if the MusicBrainz Artist is not of type Person. API path:

            /people/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        musicbrainz_artist = MusicBrainzArtist.objects.get(id=mbid)
        musicbrainz_artist_type_person = MusicBrainzArtistType.objects.get(name="Person")
        if musicbrainz_artist.type != musicbrainz_artist_type_person:
            return Response(
                {
                    "Error": (
                        f"MusicBrainz Artist '{musicbrainz_artist.name}' is not of type Person. "
                        f"Got type '{musicbrainz_artist.type}' instead."
                    )
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        try:
            instance = Person.objects.get(mbid=musicbrainz_artist.id)  # do nothing if the Person already exists
        except Person.DoesNotExist:
            instance = Person(
                id=musicbrainz_artist.gid,
                mbid=musicbrainz_artist.id,
                name=musicbrainz_artist.name,
                sort_name=musicbrainz_artist.sort_name,
                begin_date_year=musicbrainz_artist.begin_date_year,
                begin_date_month=musicbrainz_artist.begin_date_month,
                begin_date_day=musicbrainz_artist.begin_date_day,
                end_date_year=musicbrainz_artist.end_date_year,
                end_date_month=musicbrainz_artist.end_date_month,
                end_date_day=musicbrainz_artist.end_date_day,
                comment=musicbrainz_artist.comment,
                edits_pending=musicbrainz_artist.edits_pending,
                last_updated=musicbrainz_artist.last_updated,
                ended=musicbrainz_artist.ended,
            )
            if musicbrainz_artist.area is not None:
                instance.area = Area.objects.get(mbid=musicbrainz_artist.area.id)
            if musicbrainz_artist.begin_area is not None:
                instance.begin_area = Area.objects.get(mbid=musicbrainz_artist.begin_area.id)
            if musicbrainz_artist.end_area is not None:
                instance.end_area = Area.objects.get(mbid=musicbrainz_artist.end_area.id)
            if musicbrainz_artist.gender is not None:
                instance.gender = Gender.objects.get(mbid=musicbrainz_artist.gender.id)
            instance.save()

        return Response(PersonSerializer(instance=instance).data)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Person._meta.fields]

    readonly_fields = ["id", "mbid", "edits_pending", "last_updated"]
