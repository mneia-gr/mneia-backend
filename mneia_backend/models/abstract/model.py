import json
import uuid
from pathlib import Path
from typing import Dict

import yaml
from django.db import models
from django.utils.text import slugify


class Model(models.Model):
    """
    Base model from which all other models in Mneia Backend inherit.
    """

    id = models.UUIDField(
        "ID",
        primary_key=True,
        default=uuid.uuid4,
    )
    created_in_mneia = models.DateTimeField(
        "Created in Mneia",
        auto_now_add=True,  # Automatically set the field to "now" when the object is first created.
    )
    updated_in_mneia = models.DateTimeField(
        "Updated in Mneia",
        auto_now=True,  # Automatically set the field to "now" every time the object is saved.
    )

    @property
    def data_dir(self) -> Path:
        """
        The directory in which the data from an instance can be found. This is used to export an instance as a JSON
        file.
        """
        return Path.home() / "Mneia" / "mneia-data" / f"{slugify(self._meta.verbose_name_plural)}" / str(self.id)

    @property
    def json_export_file(self) -> Path:
        """The file in which the data from an instance will be exported as JSON."""
        return self.data_dir / f"{self.id}.json"

    @property
    def as_json(self) -> Dict:
        """A representation of an instance as a dictionary, as it will be exported to JSON."""
        _as_json = {}
        for field in self._meta.fields:
            if (
                isinstance(field, models.UUIDField)
                or isinstance(field, models.DateTimeField)
                or isinstance(field, models.DateField)
            ):
                # convert UUIDs and dates to strings:
                _as_json[field.name] = str(getattr(self, field.name))
            elif isinstance(field, models.ForeignKey):
                # convert foreign keys to the string ID of the related instance:
                related_instance = getattr(self, field.name)
                _as_json[field.name] = str(related_instance.id) if related_instance is not None else None
            else:
                _as_json[field.name] = getattr(self, field.name)
        return _as_json

    def export_json(self) -> None:
        """Export an instance as a JSON file."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.json_export_file.write_text(json.dumps(self.as_json, indent=2, ensure_ascii=False, sort_keys=True))

    @property
    def yaml_export_dir(self) -> Path:
        """The directory in which the data from an instance will be exported as YAML."""
        slug = slugify(self._meta.verbose_name_plural)
        return Path.home() / "Mneia" / "mneia-gr.github.io" / "collections" / f"_{slug}"

    @property
    def yaml_export_file(self) -> Path:
        """The file in which the data from an instance will be exported as YAML."""
        # yeah, yeah, we export YAML as markdown, because it's processed by Jekyll:
        return self.yaml_export_dir / f"{self.id}.md"

    def export_yaml(self) -> None:
        """
        Export an instance as YAML for processing by Jekyll. Note that `as_yaml` is different by model, and many models
        don't have it at all.
        """
        if not hasattr(self, "as_yaml"):
            return
        self.yaml_export_dir.mkdir(parents=True, exist_ok=True)
        self.yaml_export_file.write_text(f"---\n{yaml.dump(self.as_yaml, allow_unicode=True)}---\n")

    class Meta:
        abstract = True
