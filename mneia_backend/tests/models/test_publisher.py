import pytest

from mneia_backend.models.publisher import Publisher


@pytest.mark.django_db
def test_publisher_str():
    publisher = Publisher.objects.get(id="1526d9b4-cd45-4790-83c4-a7f92bbc80c4")
    assert str(publisher) == "Εκδόσεις Αιγόκερως"


@pytest.mark.django_db
def test_publisher_as_yaml():
    publisher = Publisher.objects.get(id="1526d9b4-cd45-4790-83c4-a7f92bbc80c4")
    assert publisher.as_yaml == {
        "name": "Εκδόσεις Αιγόκερως",
        "title": "Εκδόσεις Αιγόκερως",
        "references": {
            "books": [
                {
                    "book": {
                        "area": "Αθήνα",
                        "authors": [{"id": "20ea77bb-0924-4380-b7ef-2740d4126576", "name": "Σολδάτος, Γιάννης"}],
                        "edition": "Β Έκδοση",
                        "id": "f979c381-dd7b-4e8f-9b71-6ca6c6507927",
                        "name": "Ένας άνθρωπος παντός καιρού",
                        "publication_date_year": 2000,
                    },
                    "publisher": {"id": "1526d9b4-cd45-4790-83c4-a7f92bbc80c4", "name": "Εκδόσεις Αιγόκερως"},
                }
            ]
        },
    }
