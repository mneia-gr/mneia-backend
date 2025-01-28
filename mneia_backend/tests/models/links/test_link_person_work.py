import pytest

from mneia_backend.models.links.person_work import LinkPersonWork


@pytest.mark.django_db
def test_link_person_work_as_link_to_work():
    link_person_work = LinkPersonWork.objects.get(id="11111111-2222-47b6-a0b3-19f3a1cdcf45")
    assert link_person_work.as_link_to_work == {
        "link_phrase": "is the subject of",
        "work": {
            "id": "11111111-4444-4f16-90f1-290c99f233f3",
            "name": "Foo",
        },
    }


@pytest.mark.django_db
def test_link_person_work_as_link_to_person():
    link_person_work = LinkPersonWork.objects.get(id="11111111-2222-47b6-a0b3-19f3a1cdcf45")
    assert link_person_work.as_link_to_person == {
        "link_phrase": "has subject",
        "person": {
            "id": "63eec1f5-f535-46a0-9fd3-6826a4f09e5c",
            "name": "Κυβέλη",
        },
    }
