import uuid
from typing import Literal


def get_musicbrainz_identifier_type(identifier: str | int) -> Literal["gid", "name", "id"]:
    try:
        uuid.UUID(identifier)
    except (ValueError, AttributeError):
        pass
    else:
        return "gid"
    try:
        int(identifier)
    except ValueError:
        return "name"
    else:
        return "id"
