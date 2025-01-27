import pytest

from mneia_backend.utils import get_musicbrainz_identifier_type


@pytest.mark.parametrize(
    "identifier, expected",
    [
        ("1234", "id"),
        ("49daefeb-3cc5-4f8b-aa0d-26d7c83be1f8", "gid"),
        ("foo", "name"),
        # this is used in LinkAttribute:
        ("956d1ec2-33b2-4cd6-8832-1bbcd0d42661+2745d711-1ca1-4647-9971-5e208682fdcb", "name"),
    ],
)
def test_get_musicbrainz_identifier_type(identifier, expected):
    assert get_musicbrainz_identifier_type(identifier) == expected
