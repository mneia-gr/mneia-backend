import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_link_api_get_by_uuid():
    """It is possible to GET a Link by either its UUID or its MBID. Here we are testing GET by UUID."""
    api_client = APIClient()
    response = api_client.get("/links/956d1ec2-33b2-4cd6-8832-1bbcd0d42661/")  # from fixture
    assert response.status_code == 200


@pytest.mark.django_db
def test_link_api_get_by_mbid():
    """It is possible to GET a Link by either its UUID or its MBID. Here we are testing GET by MBID."""
    api_client = APIClient()
    response = api_client.get("/links/11111/")  # from fixture
    assert response.status_code == 200


@pytest.mark.django_db
def test_link_api_get_does_not_exist():
    api_client = APIClient()
    response = api_client.get("/links/12345678/")  # from fixture
    assert response.status_code == 404


@pytest.mark.django_db
def test_link_api_import_from_musicbrainz():
    api_client = APIClient()

    response = api_client.get("/links/27098/")
    assert response.status_code == 404  # assert that the Link does not exist before importing

    response = api_client.post("/links/import/", data={"mbid": 27098})
    assert response.status_code == 200  # assert that the import went well

    response = api_client.get("/links/27098/")
    assert response.status_code == 200  # assert that the Link exists after the import
