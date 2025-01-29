import pytest

from mneia_backend.models.links.magazine_issue_work import LinkMagazineIssueWork


@pytest.mark.django_db
def test_link_magazine_issue_work_as_reference():
    link_magazine_issue_work = LinkMagazineIssueWork.objects.get(id="dd11bfc9-290c-4640-87b7-17bc61e2279d")
    assert link_magazine_issue_work.as_reference == {
        "magazine": {
            "id": "0e609d69-f994-4930-8812-b188175f35d1",
            "name": "Μεγάλη Ελληνική Εγκυκλοπαίδεια",
        },
        "magazine_issue": {
            "id": "89f09153-83d8-4285-9fc7-67fb56b8ff79",
            "issue_number": "2ον Τεύχος",
            "date_published": "7 Μαρτίου 1926",
        },
        "work": {
            "id": "4adcfb27-8f2a-4122-8906-93ff18a3b9dc",
            "name": "Από το «Καπρίς»",
            "authors": [{"id": "7ea22d2b-4781-4882-af6f-15a6ca286501", "name": "Σύλβιος"}],
            "type": "Poem",
        },
        "attributes": {},
    }
