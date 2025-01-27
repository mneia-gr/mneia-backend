import rest_framework
from django.contrib import admin
from django.db import models
from django_musicbrainz_connector.models.link_attribute import LinkAttribute as MusicBrainzLinkAttribute

from mneia_backend.models import abstract
from mneia_backend.models.link import Link
from mneia_backend.models.link_attribute_type import LinkAttributeType
from mneia_backend.utils import get_musicbrainz_identifier_type


class LinkAttribute(abstract.Model):
    link = models.ForeignKey("Link", on_delete=models.PROTECT)
    attribute_type = models.ForeignKey("LinkAttributeType", verbose_name="Link Attribute", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Link Attributes"
        constraints = [models.UniqueConstraint(fields=["link", "attribute_type"], name="unique_together")]


class LinkAttributeSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = LinkAttribute
        fields = "__all__"


class LinkAttributeViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = LinkAttribute.objects.all()
    serializer_class = LinkAttributeSerializer

    def get_object(self):
        """
        Overriding the default `get_object` method of `ModelViewSet` to allow GET by either the ID, or the combination
        of Link ID and LinkAttributeType ID. The combination of Link ID and LinkAttributeType ID is unique, per the
        PostgresSQL definition in the MusicBrainz server.

        Either of these calls should work:

            GET /link-attributes/956d1ec2-33b2-4cd6-8832-1bbcd0d42661/
            GET /link-attributes/956d1ec2-33b2-4cd6-8832-1bbcd0d42661+2745d711-1ca1-4647-9971-5e208682fdcb/
        """
        pk = self.kwargs["pk"]
        pk_type = get_musicbrainz_identifier_type(pk)  # either "name" or "gid"

        if pk_type == "gid":
            params = {"id": pk}
        else:
            link_id, attribute_type_id = pk.split("+")
            params = {"link_id": link_id, "attribute_type_id": attribute_type_id}

        try:
            return LinkAttribute.objects.get(**params)
        except LinkAttribute.DoesNotExist:
            raise rest_framework.exceptions.NotFound

    @rest_framework.decorators.action(detail=False, methods=["POST"], url_path="import")
    def import_from_musicbrainz(self, request):
        """
        Custom API action to import an instance of LinkAttribute from an instance of MusicBrainzLinkAttribute. API path:

            /link-attributes/import/

        Example payload:

            {"mb_link_id": 11111, "mb_attribute_type_id": 3}
        """
        mb_link_id = request.data["mb_link_id"]
        mb_attribute_type_id = request.data["mb_attribute_type_id"]
        link = Link.objects.get(mbid=mb_link_id)
        attribute_type = LinkAttributeType.objects.get(mbid=mb_attribute_type_id)
        mb_instance = MusicBrainzLinkAttribute.objects.get(link=mb_link_id, attribute_type=mb_attribute_type_id)
        try:
            # do nothing if the instance already exists:
            instance = LinkAttribute.objects.get(link=link, attribute_type=attribute_type)
        except LinkAttribute.DoesNotExist:
            instance = LinkAttribute(
                link=link,
                attribute_type=attribute_type,
                created=mb_instance.created,
            )
            instance.save()

        return rest_framework.response.Response(LinkAttributeSerializer(instance=instance).data)


@admin.register(LinkAttribute)
class LinkAttributeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LinkAttribute._meta.fields]
    readonly_fields = ["id"]
