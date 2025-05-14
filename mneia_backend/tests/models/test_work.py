import pytest
from rest_framework.test import APIClient

from mneia_backend.models.work import Work


@pytest.mark.django_db
def test_work_str():
    work = Work.objects.get(id="4adcfb27-8f2a-4122-8906-93ff18a3b9dc")  # from fixture
    assert str(work) == "Από το «Καπρίς»"


@pytest.mark.django_db
def test_work_api_import_from_musicbrainz():
    api_client = APIClient()

    response = api_client.get("/works/864c45d9-8450-4b6f-9570-744980fba21e/")
    assert response.status_code == 404  # assert that the Work does not already exist before we import it

    response = api_client.post("/works/import/", data={"mbid": 12431814})
    assert response.status_code == 200  # import succeeded

    response = api_client.get("/works/864c45d9-8450-4b6f-9570-744980fba21e/")
    assert response.status_code == 200  # the Work exists after we import it


@pytest.mark.django_db
def test_work_as_yaml():
    work = Work.objects.get(id="4adcfb27-8f2a-4122-8906-93ff18a3b9dc")  # from fixture
    assert work.as_yaml == {
        "name": "Από το «Καπρίς»",
        "title": "Από το «Καπρίς»",
        "links": {
            "people": [
                {
                    "link_phrase": "authored by",
                    "person": {
                        "id": "7ea22d2b-4781-4882-af6f-15a6ca286501",
                        "name": "Σύλβιος",
                    },
                }
            ]
        },
        "type": "Ποίημα",
        "references": {
            "magazine-issues": [
                {
                    "attributes": {},
                    "magazine": {
                        "id": "0e609d69-f994-4930-8812-b188175f35d1",
                        "name": "Μεγάλη Ελληνική " "Εγκυκλοπαίδεια",
                    },
                    "magazine_issue": {
                        "date_published": "7 " "Μαρτίου " "1926",
                        "id": "89f09153-83d8-4285-9fc7-67fb56b8ff79",
                        "issue_number": "2ον " "Τεύχος",
                    },
                    "work": {
                        "authors": [
                            {
                                "id": "7ea22d2b-4781-4882-af6f-15a6ca286501",
                                "name": "Σύλβιος",
                                "reference_name": "Σύλβιος",
                            }
                        ],
                        "id": "4adcfb27-8f2a-4122-8906-93ff18a3b9dc",
                        "name": "Από το «Καπρίς»",
                        "type": "Ποίημα",
                    },
                }
            ]
        },
        "public-domain": True,
    }
