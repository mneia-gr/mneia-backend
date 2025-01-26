import pytest

from mneia_backend.models.magazine import Magazine


@pytest.mark.django_db
def test_magazine_str():
    magazine = Magazine.objects.get(id="54236466-7978-453d-85f8-a9c04c66e026")
    assert str(magazine) == "Μεγάλη Ελληνική Εγκυκλοπαίδεια"


@pytest.mark.django_db
def test_magazine_as_yaml():
    magazine = Magazine.objects.get(id="54236466-7978-453d-85f8-a9c04c66e026")
    assert magazine.as_yaml == {
        "name": "Μεγάλη Ελληνική Εγκυκλοπαίδεια",
    }
