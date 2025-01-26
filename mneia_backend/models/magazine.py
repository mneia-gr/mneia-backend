from django.db import models

from mneia_backend.models import abstract


class Magazine(abstract.Model):
    """
    Related schema: https://schema.org/Periodical
    """

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
