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
    }
