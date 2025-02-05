import pytest

from mneia_backend.models import Photograph


@pytest.mark.django_db
def test_photograph_str():
    photograph = Photograph.objects.get(id="b07ad067-fb07-4ced-818e-05e371264689")
    assert str(photograph) == "Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»"


@pytest.mark.django_db
def test_photograph_as_yaml():
    photograph = Photograph.objects.get(id="b07ad067-fb07-4ced-818e-05e371264689")
    assert photograph.as_yaml == {
        "name": "Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»",
        "title": "Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»",
        "description": (
            "Φωτογραφία από το πρώτο τεύχος του περιοδικού «Μεγάλη Ελληνική Εγκυκλοπαίδεια», από το 1926. "
            "Απεικονίζει την ηθοποιό Κυβέλη, τότε παντρεμένη με τον θεατρικό επιχειρηματία Κώστα Θεοδωρίδη, "
            "στην «Τρίμορφη γυναίκα» του Γρηγόριου Ξενόπουλου."
        ),
        "references": {
            "magazine_issues": [
                {
                    "magazine": {
                        "id": "0e609d69-f994-4930-8812-b188175f35d1",
                        "name": "Μεγάλη Ελληνική Εγκυκλοπαίδεια",
                    },
                    "magazine_issue": {
                        "id": "49323bf2-767c-4812-b07a-f71a596b15e5",
                        "issue_number": "1ον Τεύχος",
                        "date_published": "28 Φεβρουαρίου 1926",
                    },
                    "photograph": {
                        "id": "b07ad067-fb07-4ced-818e-05e371264689",
                        "name": "Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»",
                    },
                    "attributes": {
                        "page": "1",
                    },
                }
            ]
        },
        "links": {
            "people": [
                {
                    "link_phrase": "has subject",
                    "person": {
                        "id": "63eec1f5-f535-46a0-9fd3-6826a4f09e5c",
                        "name": "Κυβέλη",
                    },
                },
            ],
        },
    }
