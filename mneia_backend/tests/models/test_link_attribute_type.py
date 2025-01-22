import uuid

import pytest
from rest_framework.test import APIClient

from mneia_backend.models.link_attribute_type import LinkAttributeType


@pytest.mark.django_db
def test_link_attribute_type_str():
    link_attribute_type = LinkAttributeType.objects.get(id="fb570822-66e6-4558-aed8-35f76938b12b")  # from fixture
    assert str(link_attribute_type) == "page"


@pytest.mark.django_db
def test_link_attribute_type_import_from_musicbrainz():
    api_client = APIClient()

    # FIRST import test, an instance that has no parent and has itself as root:
    response = api_client.get("/link-attribute-types/d92884b7-ee0c-46d5-96f3-918196ba8c5b/")
    assert response.status_code == 404  # assert that the link attribute type does not exist before importing it

    response = api_client.post("/link-attribute-types/import/", data={"mbid": 3})
    assert response.status_code == 200  # assert that the import went well

    response = api_client.get("/link-attribute-types/d92884b7-ee0c-46d5-96f3-918196ba8c5b/")
    assert response.status_code == 200  # assert that the link attribute type exists after importing it
    assert response.data["id"] == "d92884b7-ee0c-46d5-96f3-918196ba8c5b"
    assert response.data["root"] == uuid.UUID("d92884b7-ee0c-46d5-96f3-918196ba8c5b")  # same as ID

    # SECOND import test, a second instance that has the first as both parent and root:
    response = api_client.get("/link-attribute-types/8e2a3255-87c2-4809-a174-98cb3704f1a5/")
    assert response.status_code == 404  # assert that the link attribute type does not exist before importing it

    response = api_client.post("/link-attribute-types/import/", data={"mbid": 4})
    assert response.status_code == 200  # assert that the import went well

    response = api_client.get("/link-attribute-types/8e2a3255-87c2-4809-a174-98cb3704f1a5/")
    assert response.status_code == 200  # assert that the link attribute type exists after the import
    assert response.data["root"] == uuid.UUID("d92884b7-ee0c-46d5-96f3-918196ba8c5b")  # same as FIRST import ID
    assert response.data["parent"] == uuid.UUID("d92884b7-ee0c-46d5-96f3-918196ba8c5b")  # same as FIRST import ID
