import uuid

from django.db import models


class Model(models.Model):
    id = models.UUIDField(
        "ID",
        primary_key=True,
        default=uuid.uuid4,
    )
    created_in_mneia = models.DateTimeField(
        auto_now_add=True,  # Automatically set the field to now when the object is first created.
    )
    updated_in_mneia = models.DateTimeField(
        auto_now=True,  # Automatically set the field to now every time the object is saved.
    )

    class Meta:
        abstract = True


class TypeModel(Model):
    """
    There are several "type" models in MusicBrainz that have the exact same structure, like Area Type, Artist Type, etc.
    These are abstracted here to avoid code repetition.
    """

    mbid = models.IntegerField("MBID", help_text="The MusicBrainz integer ID")
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)
    child_order = models.IntegerField("Child Order")
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
        ordering = ["name"]


class LinkModel(Model):
    """
    There are several "link" models in MusicBrainz that have the exact same structure, like Link-Recording-Work, etc.
    These are abstracted here to avoid code repetition. Note that there are "Link" models in Mneia that don't come from
    MusicBrainz, like Link-Person-Photograph.
    """

    # mbid is optional in Mneia, because there are links created locally that are not imported from MusicBrainz:
    mbid = models.IntegerField("MBID", help_text="The MusicBrainz integer ID", null=True, blank=True)
    link = models.ForeignKey("Link", on_delete=models.PROTECT)
    edits_pending = models.PositiveIntegerField("Edits Pending", default=0)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    link_order = models.PositiveIntegerField("Link Order", default=0, null=True)
    entity0_credit = models.TextField(default="", blank=True)
    entity1_credit = models.TextField(default="", blank=True)

    class Meta:
        abstract = True
