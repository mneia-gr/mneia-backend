import uuid

import pytest
from rest_framework.test import APIClient

from mneia_backend.models.person import Person


@pytest.mark.django_db
def test_person_str():
    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    assert str(person) == "Κυβέλη"


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

    response = api_client.get("/people/754a1dd2-7379-4dcb-bfdb-a03459b9f530/")
    assert response.status_code == 404  # assert that the Person does not exist before the import

    response = api_client.post("/people/import/", data={"mbid": 160715})
    assert response.status_code == 200  # assert that the import worked

    response = api_client.get("/people/754a1dd2-7379-4dcb-bfdb-a03459b9f530/")
    assert response.status_code == 200  # assert that the Person exists after the import

    # assert that the foreign key fields have the correct values:
    assert response.data["area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["begin_area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["end_area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["gender"] == uuid.UUID("93452b5a-a947-30c8-934f-6a4056b151c2")


@pytest.mark.django_db
def test_person_as_yaml():
    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    assert person.as_yaml == {
        "name": "Κυβέλη",
        "links": {
            "photographs": [
                {
                    "link_phrase": "is the subject of",
                    "photograph": {
                        "id": "b07ad067-fb07-4ced-818e-05e371264689",
                        "name": "Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»",
                    },
                }
            ],
            "works": [],
        },
    }
