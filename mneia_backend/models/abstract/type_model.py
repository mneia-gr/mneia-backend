from django.db import models

from mneia_backend.models.abstract.model import Model


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