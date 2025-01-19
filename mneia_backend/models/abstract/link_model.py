from django.db import models

from mneia_backend.models.abstract.model import Model


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
