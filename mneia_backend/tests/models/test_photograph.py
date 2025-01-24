import pytest

from mneia_backend.models import Photograph


@pytest.mark.django_db
def test_photograph_str():
    photograph = Photograph.objects.get(id="b07ad067-fb07-4ced-818e-05e371264689")
    assert str(photograph) == "Ελληνικές δόξες: Η κ. ΚΥΒΕΛΗ ΘΕΟΔΩΡΙΔΟΥ εις την «Τρίμορφη Γυναίκα»"
