import pytest

from mneia_backend.models.links.person_work import LinkPersonWork


@pytest.mark.django_db
def test_link_person_work_as_link_to_work():
    link_person_work = LinkPersonWork.objects.get(id="b5dc7d18-8d7d-4850-ace2-15be3f0520ee")
    assert link_person_work.as_link_to_work == {
        "link_phrase": "is the author of",
        "work": {
            "id": "4adcfb27-8f2a-4122-8906-93ff18a3b9dc",
            "name": "Από το «Καπρίς»",
        },
    }


@pytest.mark.django_db
def test_link_person_work_as_link_to_person():
    link_person_work = LinkPersonWork.objects.get(id="b5dc7d18-8d7d-4850-ace2-15be3f0520ee")
    assert link_person_work.as_link_to_person == {
        "link_phrase": "authored by",
        "person": {
            "id": "7ea22d2b-4781-4882-af6f-15a6ca286501",
            "name": "Σύλβιος",
        },
    }
