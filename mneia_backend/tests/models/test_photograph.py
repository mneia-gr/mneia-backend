import pytest

from mneia_backend.models import Photograph


@pytest.mark.django_db
def test_photograph_str():
    photograph = Photograph.objects.get(id="a6bade31-e909-496d-bcd8-f6cfb241365d")
    assert str(photograph) == "Το όνομα της φωτογραφίας"
