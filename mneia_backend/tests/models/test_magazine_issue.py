import pytest

from mneia_backend.models.magazine_issue import MagazineIssue


@pytest.mark.django_db
def test_magazine_issue_str():
    magazine_issue = MagazineIssue.objects.get(id="77f9eb61-c3c3-4215-8d86-2dd522a1e4cc")  # from fixture
    assert str(magazine_issue) == "Μεγάλη Ελληνική Εγκυκλοπαίδεια - Issue 1"
