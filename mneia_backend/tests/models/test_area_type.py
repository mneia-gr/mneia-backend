import datetime
import uuid

import pytest
from freezegun import freeze_time
from rest_framework.test import APIClient

from mneia_backend.models.area_type import AreaType


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
def test_area_type_str():
    area_type = AreaType.objects.get(id="06dd0ae4-8c74-30bb-b43d-95dcedf961de")  # from fixture
    assert str(area_type) == "Country"


@pytest.mark.django_db
def test_area_type_api_get():
    """Tests a simple API GET request."""
    api_client = APIClient()
    response = api_client.get("/area-types/06dd0ae4-8c74-30bb-b43d-95dcedf961de/")  # from fixture
    assert response.status_code == 200


@pytest.mark.django_db
def test_area_type_import_from_musicbrainz_new_area_type():
    """
    Test that when trying to import a new Area Type that does not already exist, the new Area Type is returned.
    """
    api_client = APIClient()

    response = api_client.get("/area-types/6fd8f29a-3d0a-32fc-980d-ea697b69da78/")
    assert response.status_code == 404  # assert that the Area Type "City" does not already exist before we import it

    response = api_client.post("/area-types/import/", data={"mbid": 3})
    assert response.status_code == 200  # import succeeded

    response = api_client.get("/area-types/6fd8f29a-3d0a-32fc-980d-ea697b69da78/")
    assert response.status_code == 200  # the Area Type exists after we import it

    # The Area Type "City" has a parent in MusicBrainz so it should have one in Mneia. This is only here for testing,
    # as the "City" object in MusicBrainz does not actually have a parent:
    assert response.data["parent"] == uuid.UUID("06dd0ae4-8c74-30bb-b43d-95dcedf961de")
