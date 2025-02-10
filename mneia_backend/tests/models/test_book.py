import pytest

from mneia_backend.models.book import Book


@pytest.mark.django_db
def test_book_str():
    book = Book.objects.get(id="f979c381-dd7b-4e8f-9b71-6ca6c6507927")
    assert str(book) == "Ένας άνθρωπος παντός καιρού"


@pytest.mark.parametrize(
    "year, month, day, expected",
    [
        (None, None, None, None),
        (2007, None, None, "2007"),
        (2007, 1, None, "Ιανουάριος 2007"),
    ],
)
@pytest.mark.django_db
def test_book_publication_date(year, month, day, expected):
    book = Book(publication_date_year=year, publication_date_month=month, publication_date_day=day)
    assert book.publication_date == expected


@pytest.mark.django_db
def test_book_as_yaml():
    book = Book.objects.get(id="f979c381-dd7b-4e8f-9b71-6ca6c6507927")
    assert book.as_yaml == {
        "name": "Ένας άνθρωπος παντός καιρού",
        "title": "Ένας άνθρωπος παντός καιρού",
        "edition": "Β Έκδοση",
        "format": "Paperback",
        "isbn": "9603221384",
        "pages_number": 302,
        "publication_date": "2000",
        "links": {
            "people": [
                {
                    "link_phrase": "was authored by",
                    "person": {
                        "id": "20ea77bb-0924-4380-b7ef-2740d4126576",
                        "name": "Γιάννης Σολδάτος",
                    },
                },
            ],
        },
        "references": {
            "publishers": [
                {
                    "book": {
                        "area": "Αθήνα",
                        "authors": [{"id": "20ea77bb-0924-4380-b7ef-2740d4126576", "name": "Σολδάτος, Γιάννης"}],
                        "edition": "Β Έκδοση",
                        "id": "f979c381-dd7b-4e8f-9b71-6ca6c6507927",
                        "name": "Ένας άνθρωπος παντός καιρού",
                        "publication_date": "2000",
                    },
                    "publisher": {"id": "1526d9b4-cd45-4790-83c4-a7f92bbc80c4", "name": "Εκδόσεις Αιγόκερως"},
                }
            ]
        },
    }
