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
