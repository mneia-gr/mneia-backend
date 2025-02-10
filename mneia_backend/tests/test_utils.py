import pytest

from mneia_backend.utils import prettify_date


@pytest.mark.parametrize(
    "year, month, day, expected",
    [
        (None, None, None, None),
        (2007, None, None, "2007"),
        (2007, 1, None, "Ιανουάριος 2007"),
        (2007, 1, 1, "1 Ιανουαρίου 2007"),
    ],
)
def test_prettify_date(year, month, day, expected):
    assert prettify_date(year, month, day) == expected
