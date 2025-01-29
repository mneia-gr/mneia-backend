import pytest

from mneia_backend.models.magazine import Magazine


@pytest.mark.django_db
def test_magazine_str():
    magazine = Magazine.objects.get(id="0e609d69-f994-4930-8812-b188175f35d1")
    assert str(magazine) == "Μεγάλη Ελληνική Εγκυκλοπαίδεια"


@pytest.mark.django_db
def test_magazine_as_yaml():
    magazine = Magazine.objects.get(id="0e609d69-f994-4930-8812-b188175f35d1")
    assert magazine.as_yaml == {
        "name": "Μεγάλη Ελληνική Εγκυκλοπαίδεια",
        "issues": [
            {
                "id": "49323bf2-767c-4812-b07a-f71a596b15e5",
                "issue_number": "1ον Τεύχος",
                "date_published": "28 Φεβρουαρίου 1926",
            },
            {
                "id": "89f09153-83d8-4285-9fc7-67fb56b8ff79",
                "issue_number": "2ον Τεύχος",
                "date_published": "7 Μαρτίου 1926",
            },
        ],
    }
