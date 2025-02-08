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
        "/foo/bar/Mneia/mneia-data/area-types/06dd0ae4-8c74-30bb-b43d-95dcedf961de/"
        "06dd0ae4-8c74-30bb-b43d-95dcedf961de.json"
    )


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_data_dir(mock_path_home):
    """
    Tests that the directory path in which an instance will be exported as JSON is correct.
    """
    mock_path_home.return_value = Path("/foo/bar/")
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    assert area_type.data_dir == Path("/foo/bar/Mneia/mneia-data/area-types/06dd0ae4-8c74-30bb-b43d-95dcedf961de/")


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
@mock.patch.object(AreaType, "data_dir")
def test_area_type_json_export(mock_data_dir, mock_json_export_file):
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    area_type.export_json()

    mock_data_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
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
    assert area_type.yaml_export_dir == Path("/foo/bar/Mneia/mneia-gr.github.io/collections/_area-types/")


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_yaml_export_file(mock_path_home):
    mock_path_home.return_value = Path("/foo/bar/")

    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture

    assert area_type.yaml_export_file == Path(
        "/foo/bar/Mneia/mneia-gr.github.io/collections/_area-types/06dd0ae4-8c74-30bb-b43d-95dcedf961de.md"
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
def test_person_yaml_export_without_content(mock_yaml_export_dir, mock_yaml_export_file):
    """Person has the `as_yaml` property, so the export should run."""

    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    person.export_yaml()

    mock_yaml_export_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_yaml_export_file.write_text.assert_called_once_with(
        "---\n"
        "links:\n"
        "  books: []\n"
        "  photographs:\n"
        "  - link_phrase: is the subject of\n"
        "    photograph:\n"
        "      id: b07ad067-fb07-4ced-818e-05e371264689\n"
        "      name: 'Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»'\n"
        "  works: []\n"
        "name: Κυβέλη\n"
        "title: Κυβέλη\n"
        "---\n\n"
    )


@pytest.mark.django_db
@mock.patch.object(Person, "content", new_callable=mock.PropertyMock)
@mock.patch.object(Person, "yaml_export_file")
@mock.patch.object(Person, "yaml_export_dir")
def test_person_yaml_export_with_content(mock_yaml_export_dir, mock_yaml_export_file, mock_content):
    """Person has the `as_yaml` property, so the export should run."""
    mock_content.return_value = "foo"

    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    person.export_yaml()

    mock_yaml_export_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_yaml_export_file.write_text.assert_called_once_with(
        "---\n"
        "links:\n"
        "  books: []\n"
        "  photographs:\n"
        "  - link_phrase: is the subject of\n"
        "    photograph:\n"
        "      id: b07ad067-fb07-4ced-818e-05e371264689\n"
        "      name: 'Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»'\n"
        "  works: []\n"
        "name: Κυβέλη\n"
        "title: Κυβέλη\n"
        "---\n"
        "\n"
        '<main class="content" itemprop="text">\n'
        "<p>foo</p>\n"
        "</main>\n"
    )


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_content_file(mock_path_home):
    mock_path_home.return_value = Path("/foo/bar/")

    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture

    assert area_type.content_file == Path(
        "/foo/bar/Mneia/mneia-data/area-types/06dd0ae4-8c74-30bb-b43d-95dcedf961de/"
        "06dd0ae4-8c74-30bb-b43d-95dcedf961de.md"
    )


@pytest.mark.django_db
def test_area_type_content_is_none():
    """If the content_file of an instance is not an existing file, then the content should be None."""
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    assert area_type.content is None


@pytest.mark.django_db
@mock.patch.object(AreaType, "content_file")
def test_area_type_content(mock_content_file, tmp_path):
    """
    If the content_file of an instance is an existing file, then the content should be its contents.

    Fixture tmp_path comes from pytest: https://docs.pytest.org/en/stable/how-to/tmp_path.html
    """
    mock_content_file.return_value = tmp_path / "temp.txt"
    mock_content_file.write_text("something")

    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    area_type.content

    mock_content_file.read_text.assert_called_once()


@pytest.mark.django_db
@mock.patch.object(Path, "home")
def test_area_type_notes_file(mock_path_home):
    mock_path_home.return_value = Path("/foo/bar/")

    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture

    assert area_type.notes_file == Path(
        "/foo/bar/Mneia/mneia-data/area-types/06dd0ae4-8c74-30bb-b43d-95dcedf961de/notes.md"
    )


@pytest.mark.django_db
@mock.patch.object(AreaType, "notes_file")
def test_area_type_notes(mock_notes_file, tmp_path):
    """
    If the notes_file of an instance is an existing file, then the notes should be its contents.

    Fixture tmp_path comes from pytest: https://docs.pytest.org/en/stable/how-to/tmp_path.html
    """
    mock_notes_file.return_value = tmp_path / "temp.txt"
    mock_notes_file.write_text("something")

    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    area_type.notes

    mock_notes_file.read_text.assert_called_once()


@pytest.mark.django_db
@mock.patch.object(Person, "notes", new_callable=mock.PropertyMock)
@mock.patch.object(Person, "yaml_export_file")
@mock.patch.object(Person, "yaml_export_dir")
def test_person_yaml_export_with_notes(mock_yaml_export_dir, mock_yaml_export_file, mock_notes):
    mock_notes.return_value = "foo"

    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    person.export_yaml()

    mock_yaml_export_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_yaml_export_file.write_text.assert_called_once_with(
        "---\n"
        "links:\n"
        "  books: []\n"
        "  photographs:\n"
        "  - link_phrase: is the subject of\n"
        "    photograph:\n"
        "      id: b07ad067-fb07-4ced-818e-05e371264689\n"
        "      name: 'Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»'\n"
        "  works: []\n"
        "name: Κυβέλη\n"
        "title: Κυβέλη\n"
        "---\n"
        "\n"
        '<section class="notes">\n'
        "<h2>Σημειώσεις</h2>\n\n"
        "<p>foo</p>\n"
        "</section>\n"
    )
