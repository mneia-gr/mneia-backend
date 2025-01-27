import pytest

from mneia_backend.models.links.person_photograph import LinkPersonPhotograph


@pytest.mark.django_db
def test_link_person_photograph_as_link_to_photograph():
    link_person_photograph = LinkPersonPhotograph.objects.get(id="feb90caf-00dc-47b6-a0b3-19f3a1cdcf45")
    assert link_person_photograph.as_link_to_photograph == {
        "link_phrase": "is the subject of",
        "photograph": {
            "id": "b07ad067-fb07-4ced-818e-05e371264689",
            "name": "Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»",
        },
    }


@pytest.mark.django_db
def test_link_person_photograph_as_link_to_person():
    link_person_photograph = LinkPersonPhotograph.objects.get(id="feb90caf-00dc-47b6-a0b3-19f3a1cdcf45")
    assert link_person_photograph.as_link_to_person == {
        "link_phrase": "has subject",
        "person": {
            "id": "63eec1f5-f535-46a0-9fd3-6826a4f09e5c",
            "name": "Κυβέλη",
        },
    }
