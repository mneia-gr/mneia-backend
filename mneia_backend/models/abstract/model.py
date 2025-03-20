import json
import uuid
from pathlib import Path
from typing import Dict, Optional

import markdown2
import yaml
from django.db import models
from django.utils.text import slugify

from mneia_backend.apps import MneiaBackendConfig


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
    def content_file(self) -> Path:
        return self.data_dir / f"{self.id}.md"

    @property
    def content(self) -> Optional[str]:
        if self.content_file.is_file():
            return self.content_file.read_text()

    @property
    def notes_file(self) -> Path:
        return self.data_dir / "notes.md"

    @property
    def notes(self) -> Optional[str]:
        if self.notes_file.is_file():
            return self.notes_file.read_text()

    @property
    def json_export_file(self) -> Path:
        """The file in which the data from an instance will be exported as JSON."""
        return self.data_dir / f"{self.id}.json"

    @property
    def as_json(self) -> Dict:
        """
        A representation of an instance as a dictionary, as it will be exported to JSON. This is formatted the same way
        that management command `dumpdata` formats instances, and the same way that text fixtures are formatted. These
        exported JSON files could be imported back into the database in case of catastrophic failure.
        """
        _as_json = {
            "model": f"{MneiaBackendConfig.name}.{self.__class__.__name__.lower()}",
            "pk": str(self.id),
            "fields": {},
        }
        for field in self._meta.fields:
            if field.name == "id":
                continue
            if (
                isinstance(field, models.UUIDField)
                or isinstance(field, models.DateTimeField)
                or isinstance(field, models.DateField)
            ):
                # convert UUIDs and dates to strings:
                _as_json["fields"][field.name] = str(getattr(self, field.name))
            elif isinstance(field, models.ForeignKey):
                # convert foreign keys to the string ID of the related instance:
                related_instance = getattr(self, field.name)
                _as_json["fields"][field.name] = str(related_instance.id) if related_instance is not None else None
            else:
                _as_json["fields"][field.name] = getattr(self, field.name)
        return _as_json

    def export_json(self) -> None:
        """Export an instance as a JSON file."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.json_export_file.write_text(json.dumps(self.as_json, indent=2, ensure_ascii=False, sort_keys=True))

    @property
    def yaml_export_dir(self) -> Path:
        """The directory in which the data from an instance will be exported as YAML."""
        slug = slugify(self._meta.verbose_name_plural)
        return Path.home() / "Mneia" / "mneia-jekyll" / "collections" / f"_{slug}"

    @property
    def yaml_export_file(self) -> Path:
        """The file in which the data from an instance will be exported as YAML."""
        # yeah, yeah, we export YAML as markdown, because it's processed by Jekyll:
        return self.yaml_export_dir / f"{self.id}.md"

    def export_yaml(self) -> None:
        """
        Export an instance as YAML for processing by Jekyll. Note that `as_yaml` is different by model, and many models
        don't have it at all.

        TODO: This is awkward, mixing data and logic... part of the HTML DOM is here, and part is in Jekyll templates...
        """
        if not hasattr(self, "as_yaml"):
            return
        yaml_export = f"---\n{yaml.dump(self.as_yaml, allow_unicode=True)}---\n\n"
        if self.content is not None:
            yaml_export += f'<main class="content" itemprop="text">\n{markdown2.markdown(self.content)}</main>\n'
        if self.notes is not None:
            yaml_export += '<section class="notes">\n'
            yaml_export += f"<h2>Σημειώσεις</h2>\n\n{markdown2.markdown(self.notes)}"
            yaml_export += "</section>\n"
        self.yaml_export_dir.mkdir(parents=True, exist_ok=True)
        self.yaml_export_file.write_text("".join(yaml_export))

    class Meta:
        abstract = True
