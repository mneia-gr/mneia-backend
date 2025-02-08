import pytest

from mneia_backend.models.book import Book


@pytest.mark.django_db
def test_book_str():
    book = Book.objects.get(id="f979c381-dd7b-4e8f-9b71-6ca6c6507927")
    assert str(book) == "Ένας άνθρωπος παντός καιρού"


@pytest.mark.django_db
def test_book_as_yaml():
    book = Book.objects.get(id="f979c381-dd7b-4e8f-9b71-6ca6c6507927")
    assert book.as_yaml == {
        "name": "Ένας άνθρωπος παντός καιρού",
        "title": "Ένας άνθρωπος παντός καιρού",
        "edition": "2η έκδοση",
        "format": "Paperback",
        "isbn": "9603221384",
        "pages_number": 302,
        "publication_date_year": 2000,
    }
