import datetime
import uuid
from pathlib import Path
from unittest import mock

import pytest
from freezegun import freeze_time

from mneia_backend.models.area_type import AreaType
from mneia_backend.models.person import Person


def test_area_type_id_is_uuid():
    """
    Tests that the automatically generated ID for a new instance is a UUID. The functionality tested here comes from the
    abstract model in `mneia_backend.models.abstract.Model`.
    """
    area_type = AreaType(name="Test Area Type")
    assert isinstance(area_type.id, uuid.UUID)


@pytest.mark.django_db
def test_area_type_created_and_updated_timestamp():
    """
    Tests that the automatically generated timestamp fields for a new instance are created and updated correctly. The
    functionality tested here comes from the abstract model in `mneia_backend.models.abstract.Model`.
    """

    # When the instance is first created, both timestamps are the same:
    with freeze_time("2025-01-10 13:09:00"):
        area_type = AreaType.objects.create(name="Test Area Type", mbid=0, child_order=0)
        assert area_type.created_in_mneia == datetime.datetime(2025, 1, 10, 13, 9, 0, tzinfo=datetime.timezone.utc)
        assert area_type.updated_in_mneia == datetime.datetime(2025, 1, 10, 13, 9, 0, tzinfo=datetime.timezone.utc)

    # When the instance is updated, only the "updated" timestamp changes:
    with freeze_time("2025-01-10 13:13:00"):
        area_type.name = "Updated Test Area Type"
        area_type.save()
        assert area_type.created_in_mneia == datetime.datetime(2025, 1, 10, 13, 9, 0, tzinfo=datetime.timezone.utc)
        assert area_type.updated_in_mneia == datetime.datetime(2025, 1, 10, 13, 13, 0, tzinfo=datetime.timezone.utc)


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_json_export_file(mock_path_home):
    mock_path_home.return_value = Path("/foo/bar/")

    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture

    assert area_type.json_export_file == Path(
        "/foo/bar/Mneia/mneia-data/area-types/06dd0ae4-8c74-30bb-b43d-95dcedf961de.json"
    )


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_json_export_dir(mock_path_home):
    """
    Tests that the directory path in which an instance will be exported as JSON is correct.
    """
    mock_path_home.return_value = Path("/foo/bar/")
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    assert area_type.json_export_dir == Path("/foo/bar/Mneia/mneia-data/area-types/")


@pytest.mark.django_db
def test_area_type_as_json():
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    assert area_type.as_json == {
        "id": "06dd0ae4-8c74-30bb-b43d-95dcedf961de",
        "mbid": 1,
        "name": "Country",
        "parent": None,
        "child_order": 1,
        "description": "Country is used for areas included (or previously included) in ISO 3166-1, e.g. United States.",
        "created_in_mneia": "2025-01-10 13:42:00+00:00",
        "updated_in_mneia": "2025-01-10 13:42:00+00:00",
    }


@pytest.mark.django_db
@mock.patch.object(AreaType, "json_export_file")
@mock.patch.object(AreaType, "json_export_dir")
def test_area_type_json_export(mock_json_export_dir, mock_json_export_file):
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    area_type.export_json()

    mock_json_export_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_json_export_file.write_text.assert_called_once_with(
        '{\n  "child_order": 1,\n  "created_in_mneia": "2025-01-10 13:42:00+00:00",\n  "description": '
        '"Country is used for areas included (or previously included) in ISO 3166-1, e.g. United States.",\n  '
        '"id": "06dd0ae4-8c74-30bb-b43d-95dcedf961de",\n  "mbid": 1,\n  "name": "Country",\n  "parent": null,\n  '
        '"updated_in_mneia": "2025-01-10 13:42:00+00:00"\n}'
    )


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_yaml_export_dir(mock_path_home):
    """
    Tests that the directory path in which an instance will be exported as YAML is correct.
    """
    mock_path_home.return_value = Path("/foo/bar/")
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    assert area_type.yaml_export_dir == Path("/foo/bar/Mneia/mneia-gr.github.io/collections/_area_types/")


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_yaml_export_file(mock_path_home):
    mock_path_home.return_value = Path("/foo/bar/")

    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture

    assert area_type.yaml_export_file == Path(
        "/foo/bar/Mneia/mneia-gr.github.io/collections/_area_types/06dd0ae4-8c74-30bb-b43d-95dcedf961de.md"
    )


@pytest.mark.django_db
@mock.patch.object(AreaType, "yaml_export_file")
@mock.patch.object(AreaType, "yaml_export_dir")
def test_area_type_yaml_export(mock_yaml_export_dir, mock_yaml_export_file):
    """AreaType does not have the `as_yaml` property, so the export should do nothing."""
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    area_type.export_yaml()

    mock_yaml_export_dir.mkdir.assert_not_called()
    mock_yaml_export_file.write_text.assert_not_called()


@pytest.mark.django_db
@mock.patch.object(Person, "yaml_export_file")
@mock.patch.object(Person, "yaml_export_dir")
def test_person_yaml_export(mock_yaml_export_dir, mock_yaml_export_file):
    """Person has the `as_yaml` property, so the export should run."""

    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    person.export_yaml()

    mock_yaml_export_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_yaml_export_file.write_text.assert_called_once_with("---\nname: Κυβέλη\n---\n")
