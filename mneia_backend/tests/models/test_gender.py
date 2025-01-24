import uuid

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_gender_import_from_musicbrainz():
    """
    Test importing a Gender that does not already exist.
    """
    api_client = APIClient()

    response = api_client.get("/genders/36d3d30a-839d-3eda-8cb3-29be4384e4a9/")
    assert response.status_code == 404  # assert that the Gender "Male" does not already exist before we import it

    response = api_client.post("/genders/import/", data={"mbid": 1})
    assert response.status_code == 200  # assert that import succeeded

    response = api_client.get("/genders/36d3d30a-839d-3eda-8cb3-29be4384e4a9/")
    assert response.status_code == 200  # the Gender exists after we import it
    assert response.data["name"] == "Male"


@pytest.mark.django_db
def test_gender_with_parent_import_from_musicbrainz():
    """
    Test importing a Gender that has a "parent". This is for testing only, since practically genders in MusicBrainz
    don't have parents.
    """
    api_client = APIClient()

    # first, import the fake parent gender as defined in the fixture:
    api_client.post("/genders/import/", data={"mbid": 100})

    # then, import the child gender:
    api_client.post("/genders/import/", data={"mbid": 101})

    # finally, retrieve the child and check for parent:
    response = api_client.get("/genders/86562cca-1cbd-40f6-95b5-c3a341f7531d/")
    assert response.data["parent"] == uuid.UUID("ae2e7ad4-e0fc-4c57-be02-df6b29d83b1e")
