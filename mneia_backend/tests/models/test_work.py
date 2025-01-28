import pytest
from rest_framework.test import APIClient

from mneia_backend.models.work import Work


@pytest.mark.django_db
def test_work_str():
    work = Work.objects.get(id="11111111-4444-4f16-90f1-290c99f233f3")  # from fixture
    assert str(work) == "Foo"


@pytest.mark.django_db
def test_work_api_import_from_musicbrainz():
    api_client = APIClient()

    response = api_client.get("/works/864c45d9-8450-4b6f-9570-744980fba21e/")
    assert response.status_code == 404  # assert that the Work does not already exist before we import it

    response = api_client.post("/works/import/", data={"mbid": 12431814})
    assert response.status_code == 200  # import succeeded

    response = api_client.get("/works/864c45d9-8450-4b6f-9570-744980fba21e/")
    assert response.status_code == 200  # the Work exists after we import it
