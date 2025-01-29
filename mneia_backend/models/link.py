import rest_framework
from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models.link import Link as MusicBrainzLink
from django_musicbrainz_connector.utils import get_musicbrainz_identifier_type

from mneia_backend.models import abstract
from mneia_backend.models.link_type import LinkType


class Link(abstract.Model):
    mbid = models.IntegerField("MBID", null=True)  # optional, because there are links specific to Mneia
    link_type = models.ForeignKey("LinkType", verbose_name="Type", related_name="links", on_delete=models.PROTECT)
    begin_date_year = models.SmallIntegerField("Begin Date Year", null=True, blank=True)
    begin_date_month = models.SmallIntegerField("Begin Date Month", null=True, blank=True)
    begin_date_day = models.SmallIntegerField("Begin Date Day", null=True, blank=True)
    end_date_year = models.SmallIntegerField("End Date Year", null=True, blank=True)
    end_date_month = models.SmallIntegerField("End Date Month", null=True, blank=True)
    end_date_day = models.SmallIntegerField("End Date Day", null=True, blank=True)
    attribute_count = models.IntegerField("Attribute Count", default=0)
    created = models.DateTimeField("Created", auto_now_add=True)
    ended = models.BooleanField("Ended?", default=False)

    @property
    def calculated_attribute_count(self) -> int:
        """
        The Link model has an `attribute_count` field. This calculated attribute count is used to run an integration
        test, to assert the consistency between the two.
        """
        return self.link_attributes.count()

    @property
    def explanation(self) -> str:
        """
        This helpful string is displayed in the Admin interface, it helps understand the purpose of a Link.
        """
        _ = [
            f"Link of type '{self.link_type.name}'",
            f"between '{self.link_type.entity_type0}'",
            f"and '{self.link_type.entity_type1}'",
        ]
        if self.link_attributes.count() == 0:
            _.append("with no attributes")
        elif self.link_attributes.count() == 1:
            _.append("with attribute")
        else:
            _.append("with attributes")

        for link_attribute in self.link_attributes.all():
            link_attribute_type = link_attribute.attribute_type
            link_text_attribute_type = link_attribute_type.link_text_attribute_types.first()
            link_attribute_text_value = link_text_attribute_type.link_attribute_text_values.filter(link=self)[0]
            _.append(f"{link_attribute_type.name}={link_attribute_text_value.text_value}")

        return " ".join(_)

    class Meta:
        verbose_name_plural = "Links"


class LinkSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"


class LinkViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def get_object(self):
        """
        Overriding the default `get_object` method of `ModelViewSet` to allow GET by either the Link ID (a UUID that is
        local to Mneia, it does not exist on the MusicBrainz Link model), or the MBID (the numeric ID from MusicBrainz).

        Either of these calls should work:

            GET /links/956d1ec2-33b2-4cd6-8832-1bbcd0d42661/
            GET /links/159
        """
        pk = self.kwargs["pk"]
        mb_pk_type = get_musicbrainz_identifier_type(pk)  # either "id" or "gid"
        if mb_pk_type == "id":
            pk_type = "mbid"
        else:
            pk_type = "id"
        params = {pk_type: pk}
        try:
            return Link.objects.get(**params)
        except Link.DoesNotExist:
            raise rest_framework.exceptions.NotFound

    @rest_framework.decorators.action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of Link from an instance of MusicBrainzLink. API path:

            /links/import/

        Example payload:

            {"mbid": 1}
        """
        mbid = request.data["mbid"]
        mb_instance = MusicBrainzLink.objects.get(id=mbid)
        try:
            instance = Link.objects.get(mbid=mb_instance.id)  # for now, do nothing if the Link already exists
        except Link.DoesNotExist:
            instance = Link(
                mbid=mb_instance.id,
                link_type=LinkType.objects.get(mbid=mb_instance.link_type.id),
                begin_date_year=mb_instance.begin_date_year,
                begin_date_month=mb_instance.begin_date_month,
                begin_date_day=mb_instance.begin_date_day,
                end_date_year=mb_instance.end_date_year,
                end_date_month=mb_instance.end_date_month,
                end_date_day=mb_instance.end_date_day,
                attribute_count=mb_instance.attribute_count,
                created=mb_instance.created,
                ended=mb_instance.ended,
            )
            instance.save()

        return rest_framework.response.Response(LinkSerializer(instance=instance).data)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["explanation", "link_type", "attribute_count", "calculated_attribute_count"]
    readonly_fields = ["id", "mbid", "explanation", "calculated_attribute_count"]
