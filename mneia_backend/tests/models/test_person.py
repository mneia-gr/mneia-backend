import uuid
from unittest import mock

import pytest
from freezegun import freeze_time
from rest_framework.test import APIClient

from mneia_backend.models.person import Person


@pytest.mark.django_db
def test_person_str():
    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    assert str(person) == "Κυβέλη"


@mock.patch("mneia_backend.models.person.prettify_date", return_value="fake begin date")
@pytest.mark.django_db
def test_person_begin_date(mock_prettify_date):
    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    begin_date = person.begin_date

    mock_prettify_date.assert_called_once_with(person.begin_date_year, person.begin_date_month, person.begin_date_day)
    assert begin_date == "fake begin date"


@mock.patch("mneia_backend.models.person.prettify_date", return_value="fake end date")
@pytest.mark.django_db
def test_person_end_date(mock_prettify_date):
    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")  # from fixture
    end_date = person.end_date

    mock_prettify_date.assert_called_once_with(person.end_date_year, person.end_date_month, person.end_date_day)
    assert end_date == "fake end date"


@pytest.mark.django_db
def test_person_api_import_group_returns_422():
    """
    Tests that an "HTTP 422 Unprocessable Entity" status code is returned when a request is made to import a MusicBrainz
    Artist into the Person model, but the MusicBrainz Artist is not of type Person in the MusicBrainz database.
    """
    api_client = APIClient()
    response = api_client.post("/people/import/", {"mbid": 198626})  # from fixture, this is a Group not a Person
    assert response.status_code == 422


@pytest.mark.django_db
def test_person_api_import_by_mbid():
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
def test_person_api_import_by_gid():
    api_client = APIClient()

    response = api_client.get("/people/754a1dd2-7379-4dcb-bfdb-a03459b9f530/")
    assert response.status_code == 404  # assert that the Person does not exist before the import

    response = api_client.post("/people/import/", data={"id": "754a1dd2-7379-4dcb-bfdb-a03459b9f530"})
    assert response.status_code == 200  # assert that the import worked

    response = api_client.get("/people/754a1dd2-7379-4dcb-bfdb-a03459b9f530/")
    assert response.status_code == 200  # assert that the Person exists after the import

    # assert that the foreign key fields have the correct values:
    assert response.data["area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["begin_area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["end_area"] == uuid.UUID("803db0ca-b6ed-3bbc-aeb8-f89efd0a2168")
    assert response.data["gender"] == uuid.UUID("93452b5a-a947-30c8-934f-6a4056b151c2")


@pytest.mark.django_db
def test_person_api_import_by_name():
    api_client = APIClient()

    response = api_client.get("/people/754a1dd2-7379-4dcb-bfdb-a03459b9f530/")
    assert response.status_code == 404  # assert that the Person does not exist before the import

    response = api_client.post("/people/import/", data={"name": "Ρόζα Εσκενάζυ"})
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
        "title": "Κυβέλη",
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
            "books": [],
        },
    }


@freeze_time("2025-03-20 12:54:00")
@pytest.mark.django_db
def test_person_end_date_year_interval():
    person = Person.objects.get(id="7ea22d2b-4781-4882-af6f-15a6ca286501")  # from fixture
    assert person.end_date_year_interval == 77

    person = Person.objects.get(id="63eec1f5-f535-46a0-9fd3-6826a4f09e5c")
    assert person.end_date_year_interval is None
