import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_link_attribute_api_get_by_id():
    api_client = APIClient()
    response = api_client.get("/link-attributes/e9ea0509-9095-476a-a407-dac4683d28cf/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_link_attribute_api_get_by_link_id_and_attribute_type_id():
    api_client = APIClient()
    response = api_client.get(
        "/link-attributes/956d1ec2-33b2-4cd6-8832-1bbcd0d42661+fb570822-66e6-4558-aed8-35f76938b12b/"
    )
    assert response.status_code == 200
    assert response.data["id"] == "e9ea0509-9095-476a-a407-dac4683d28cf"


@pytest.mark.django_db
def test_link_attribute_api_get_by_id_not_found():
    api_client = APIClient()
    response = api_client.get("/link-attributes/11111111-2222-3333-a407-dac4683d28cf/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_link_attribute_api_import_from_musicbrainz():
    api_client = APIClient()

    response = api_client.get(
        "/link-attributes/11111111-2222-4cd6-8832-1bbcd0d42661+9f63c4ba-b76f-40d5-9e99-2fb08bd4c286/"
    )
    assert response.status_code == 404  # assert that the link attribute does not exist before importing

    response = api_client.post("/link-attributes/import/", data={"mb_link_id": 11111, "mb_attribute_type_id": 22222})
    assert response.status_code == 200  # assert that the import went well

    response = api_client.get(
        "/link-attributes/11111111-2222-4cd6-8832-1bbcd0d42661+9f63c4ba-b76f-40d5-9e99-2fb08bd4c286/"
    )
    assert response.status_code == 200  # assert that the link attribute exists after importing
