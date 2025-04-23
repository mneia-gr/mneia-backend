import pytest
from django.core.exceptions import ValidationError

from mneia_backend.models.book import Book, validate_isbn


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
                        "editors": [],
                        "id": "f979c381-dd7b-4e8f-9b71-6ca6c6507927",
                        "name": "Ένας άνθρωπος παντός καιρού",
                        "publication_date": "2000",
                        "isbn": {
                            "hyphenated": "960-322-138-4",
                        },
                    },
                    "publisher": {"id": "1526d9b4-cd45-4790-83c4-a7f92bbc80c4", "name": "Εκδόσεις Αιγόκερως"},
                }
            ]
        },
    }


@pytest.mark.parametrize(
    "value",
    [
        ("960211634X"),
        ("9789606882333"),
        (None),
    ],
)
def test_validate_isbn_is_valid(value):
    """Valid ISBN or `None` should return `None`"""
    assert validate_isbn(value) is None


@pytest.mark.parametrize(
    "value, match",
    [
        ("asd", "Value asd is neither 10 nor 13 digits long, got 3 digits."),
        ("FOOBAR163X", "Value FOOBAR163X is not valid ISBN10."),
        ("FOOBAR6882333", "Value FOOBAR6882333 is not valid ISBN13."),
    ],
)
def test_validate_isbn_is_not_valid(value, match):
    """Invalid ISBN values should raise ValidationError."""
    with pytest.raises(ValidationError, match=match):
        validate_isbn(value)
