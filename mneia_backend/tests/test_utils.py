import pytest

from mneia_backend.utils import get_musicbrainz_identifier_type


@pytest.mark.parametrize(
    "identifier, expected",
    [
        ("1234", "id"),
        ("49daefeb-3cc5-4f8b-aa0d-26d7c83be1f8", "gid"),
        ("foo", "name"),
    ],
)
def test_get_musicbrainz_identifier_type(identifier, expected):
    assert get_musicbrainz_identifier_type(identifier) == expected
