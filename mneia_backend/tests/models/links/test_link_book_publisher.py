import pytest

from mneia_backend.models.links.book_publisher import LinkBookPublisher


@pytest.mark.django_db
def test_link_book_publisher_as_link_to_book():
    link_book_publisher = LinkBookPublisher.objects.get(id="a002930a-d045-4e05-bb65-27ee94300b10")
    assert link_book_publisher.as_link_to_book == {
        "link_phrase": "published",
        "book": {
            "id": "f979c381-dd7b-4e8f-9b71-6ca6c6507927",
            "name": "Ένας άνθρωπος παντός καιρού",
        },
    }


@pytest.mark.django_db
def test_link_book_publisher_as_link_to_publisher():
    link_book_publisher = LinkBookPublisher.objects.get(id="a002930a-d045-4e05-bb65-27ee94300b10")
    assert link_book_publisher.as_link_to_publisher == {
        "link_phrase": "was published by",
        "publisher": {
            "id": "1526d9b4-cd45-4790-83c4-a7f92bbc80c4",
            "name": "Εκδόσεις Αιγόκερως",
        },
    }


@pytest.mark.django_db
def test_link_book_publisher_as_reference():
    link_book_publisher = LinkBookPublisher.objects.get(id="a002930a-d045-4e05-bb65-27ee94300b10")
    assert link_book_publisher.as_reference == {
        "book": {
            "id": "f979c381-dd7b-4e8f-9b71-6ca6c6507927",
            "name": "Ένας άνθρωπος παντός καιρού",
            "publication_date": "2000",
            "authors": [
                {
                    "id": "20ea77bb-0924-4380-b7ef-2740d4126576",
                    "name": "Σολδάτος, Γιάννης",
                },
            ],
            "editors": [],
            "edition": "Β Έκδοση",
            "area": "Αθήνα",
            "isbn": "9603221384",
        },
        "publisher": {
            "id": "1526d9b4-cd45-4790-83c4-a7f92bbc80c4",
            "name": "Εκδόσεις Αιγόκερως",
        },
    }
