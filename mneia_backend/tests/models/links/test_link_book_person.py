import pytest

from mneia_backend.models.links.book_person import LinkBookPerson


@pytest.mark.django_db
def test_link_book_person_as_link_to_book():
    link_book_person = LinkBookPerson.objects.get(id="4dd2a868-02d8-40e0-a607-677a91ce1cf5")
    assert link_book_person.as_link_to_book == {
        "link_phrase": "is the author of",
        "book": {
            "id": "f979c381-dd7b-4e8f-9b71-6ca6c6507927",
            "name": "Ένας άνθρωπος παντός καιρού",
        },
    }


@pytest.mark.django_db
def test_link_book_person_as_link_to_person():
    link_book_person = LinkBookPerson.objects.get(id="4dd2a868-02d8-40e0-a607-677a91ce1cf5")
    assert link_book_person.as_link_to_person == {
        "link_phrase": "was authored by",
        "person": {
            "id": "20ea77bb-0924-4380-b7ef-2740d4126576",
            "name": "Γιάννης Σολδάτος",
        },
    }
