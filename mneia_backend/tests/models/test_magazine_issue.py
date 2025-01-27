import pytest

from mneia_backend.models.magazine_issue import MagazineIssue


@pytest.mark.django_db
def test_magazine_issue_str():
    magazine_issue = MagazineIssue.objects.get(id="49323bf2-767c-4812-b07a-f71a596b15e5")  # from fixture
    assert str(magazine_issue) == "Μεγάλη Ελληνική Εγκυκλοπαίδεια - Issue 1ον Τεύχος"


@pytest.mark.django_db
def test_magazine_issue_as_yaml():
    magazine = MagazineIssue.objects.get(id="49323bf2-767c-4812-b07a-f71a596b15e5")  # from fixture
    assert magazine.as_yaml == {
        "issue_number": "1ον Τεύχος",
        "date_published": "28 Φεβρουαρίου 1926",
        "magazine": {
            "id": "0e609d69-f994-4930-8812-b188175f35d1",
            "name": "Μεγάλη Ελληνική Εγκυκλοπαίδεια",
        },
        "references": {
            "photographs": [
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
    }
