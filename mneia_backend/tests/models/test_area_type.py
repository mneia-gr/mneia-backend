import uuid

import pytest
from rest_framework.test import APIClient

from mneia_backend.models.area_type import AreaType


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
