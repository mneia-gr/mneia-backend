import uuid

import pytest
from rest_framework.test import APIClient

from mneia_backend.models.person import Person


@pytest.mark.django_db
def test_person_str():
    person = Person.objects.get(id="482a86e0-4d49-4d26-8406-3d06f01f0285")  # from fixture
    assert str(person) == "Μάρκος Βαμβακάρης"


@pytest.mark.django_db
def test_person_api_import_raises_integrity_error():
    """
    Tests that an "HTTP 422 Unprocessable Entity" status code is returned when a request is made to import a MusicBrainz
    Artist into the Person model, but the MusicBrainz Artist is not of type Person in the MusicBrainz database.
    """
    api_client = APIClient()
    response = api_client.post("/people/import/", {"mbid": 198626})  # from fixture, this is a Group not a Person
    assert response.status_code == 422


@pytest.mark.django_db
def test_person_api_import():
    api_client = APIClient()

    response = api_client.get("/people/64bf8e96-63e3-4557-8a84-c0df7ad8d18d/")
    assert response.status_code == 404  # assert that the Person does not exist before the import

    response = api_client.post("/people/import/", data={"mbid": 205524})
    assert response.status_code == 200  # assert that the import worked

    response = api_client.get("/people/64bf8e96-63e3-4557-8a84-c0df7ad8d18d/")
    assert response.status_code == 200  # assert that the Person exists after the import

    # assert that the foreign key fields have the correct values:
    assert response.data["area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["begin_area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["end_area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["gender"] == uuid.UUID("36d3d30a-839d-3eda-8cb3-29be4384e4a9")
