import uuid

import pytest
from rest_framework.test import APIClient

from mneia_backend.models import LinkType


@pytest.mark.django_db
def test_link_type_str():
    link_type = LinkType.objects.get(id="a3005666-a872-32c3-ad06-98af558e99b0")
    assert str(link_type) == "performance: recording -> work"


@pytest.mark.django_db
def test_link_type_import_from_musicbrainz():
    api_client = APIClient()

    response = api_client.get("/link-types/44598c7e-01f9-438b-950a-183720a2cbbe/")
    assert response.status_code == 404  # assert that the Link Type does not exist before the import

    response = api_client.post("/link-types/import/", data={"mbid": 257})
    assert response.status_code == 200  # assert that the import worked

    response = api_client.get("/link-types/44598c7e-01f9-438b-950a-183720a2cbbe/")
    assert response.status_code == 200  # assert that the Link Type exists after the import

    response = api_client.post("/link-types/import/", data={"mbid": 255})  # import another Link Type, one with "parent"
    assert response.data["parent"] == uuid.UUID("44598c7e-01f9-438b-950a-183720a2cbbe")
