import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_link_api_get_by_uuid():
    api_client = APIClient()
    response = api_client.get("/links/b30318e0-f672-466c-95c4-c9a7c51069fa/")  # from fixture
    assert response.status_code == 200


@pytest.mark.django_db
def test_link_api_get_by_mbid():
    api_client = APIClient()
    response = api_client.get("/links/159/")  # from fixture
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
