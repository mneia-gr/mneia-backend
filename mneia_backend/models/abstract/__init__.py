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
    There are several models in MusicBrainz that have the exact same structure, like Area Type, Artist Type, etc. These
    are abstracted here to avoid code repetition.
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
