from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models import LinkType as MusicBrainzLinkType
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mneia_backend.models import abstract

ENTITY_0_CHOICES = [
    ("person", "person"),
    ("magazine_issue", "magazine_issue"),
]

ENTITY_1_CHOICES = [
    ("photograph", "photograph"),
]


class LinkType(abstract.Model):
    """
    Example Link Type from the MusicBrainz DB:

    id                  = 278
    parent              = None
    child_order         = 0
    gid                 = a3005666-a872-32c3-ad06-98af558e99b0
    entity_type0        = recording
    entity_type1        = work
    name                = performance
    description         = This is used to link works to their recordings.
    link_phrase         = {acappella:a cappella} {live} {medley:medley including a} {partial} {instrumental} {cover}
                          {karaoke} {demo} recording of
    reverse_link_phrase = {acappella:a cappella} {live} {medley:medleys including} {partial} {instrumental} {cover}
                          {karaoke} {demo} recordings
    long_link_phrase    = is {acappella:an|a} {acappella:a cappella} {live} {medley:medley including a} {partial}
                          {instrumental} {cover} {karaoke} {demo} recording of
    last_updated        = 2024-11-06 13:46:01.649493+00
    is_deprecated       = False
    has_dates           = True
    entity0_cardinality = 0
    entity1_cardinality = 1
    """

    mbid = models.IntegerField("MBID", null=True)  # optional, because there are link types specific to Mneia
    parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)
    child_order = models.IntegerField("Child Order", default=0)
    entity_type0 = models.CharField("Entity Type 0", max_length=50, choices=ENTITY_0_CHOICES)
    entity_type1 = models.CharField("Entity Type 1", max_length=50, choices=ENTITY_1_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField()
    link_phrase = models.CharField("Link Phrase", max_length=255)
    reverse_link_phrase = models.CharField("Reverse Link Phrase", max_length=255)
    long_link_phrase = models.CharField("Long Link Phrase", max_length=255)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    is_deprecated = models.BooleanField("Is Deprecated?", default=False)
    has_dates = models.BooleanField("Has Dates?", default=True)
    entity0_cardinality = models.SmallIntegerField("Entity 0 Cardinality", default=0)
    entity1_cardinality = models.SmallIntegerField("Entity 1 Cardinality", default=0)

    def __str__(self) -> str:
        return f"{self.name}: {self.entity_type0} -> {self.entity_type1}"

    class Meta:
        verbose_name_plural = "Link Types"


class LinkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkType
        fields = "__all__"


class LinkTypeViewSet(viewsets.ModelViewSet):
    queryset = LinkType.objects.all()
    serializer_class = LinkTypeSerializer

    @action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of Link Type from an instance of MusicBrainzLinkType. API path:

            /link-types/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzLinkType.objects.get(id=mbid)
        try:
            instance = LinkType.objects.get(mbid=mb_instance.id)  # for now, do nothing if the Link Type already exists
        except LinkType.DoesNotExist:
            instance = LinkType(
                id=mb_instance.gid,
                mbid=mb_instance.id,
                child_order=mb_instance.child_order,
                entity_type0=mb_instance.entity_type0,
                entity_type1=mb_instance.entity_type1,
                name=mb_instance.name,
                description=mb_instance.description,
                link_phrase=mb_instance.link_phrase,
                reverse_link_phrase=mb_instance.reverse_link_phrase,
                long_link_phrase=mb_instance.long_link_phrase,
                last_updated=mb_instance.last_updated,
                is_deprecated=mb_instance.is_deprecated,
                has_dates=mb_instance.has_dates,
                entity0_cardinality=mb_instance.entity0_cardinality,
                entity1_cardinality=mb_instance.entity1_cardinality,
            )
            if mb_instance.parent is not None:
                instance.parent = LinkType.objects.get(mbid=mb_instance.parent.id)
            instance.save()

        return Response(LinkTypeSerializer(instance=instance).data)


@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkType._meta.fields]

    readonly_fields = [
        "id",
        "mbid",
        "parent",
        "child_order",
        "is_deprecated",
        "has_dates",
        "entity0_cardinality",
        "entity1_cardinality",
    ]
