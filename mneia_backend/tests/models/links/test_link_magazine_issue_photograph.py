import pytest

from mneia_backend.models.links.magazine_issue_photograph import LinkMagazineIssuePhotograph


@pytest.mark.django_db
def test_link_magazine_issue_photograph_as_reference():
    link_magazine_issue_photograph = LinkMagazineIssuePhotograph.objects.get(id="8f3659e5-9597-4374-a821-52a0fb284e1d")
    assert link_magazine_issue_photograph.as_reference == {
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
