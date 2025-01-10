import pytest
from rest_framework.test import APIClient

from mneia_backend.models.area import Area


@pytest.mark.django_db
def test_area_str():
    area = Area.objects.get(id="803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")  # from fixture
    assert str(area) == "Greece"


@pytest.mark.django_db
def test_area_import_from_musicbrainz():
    api_client = APIClient()

    response = api_client.get("/areas/390b05d4-11ec-3bce-a343-703a366b34a5/")
    assert response.status_code == 404  # assert that the Area "Ireland" does not already exist before we import it

    response = api_client.post("/areas/import/", data={"mbid": 103})
    assert response.status_code == 200  # assert that the import worked

    response = api_client.get("/areas/390b05d4-11ec-3bce-a343-703a366b34a5/")
    assert response.status_code == 200
    assert response.data["name"] == "Ireland"
