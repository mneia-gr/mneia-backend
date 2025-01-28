import uuid

import pytest
from rest_framework.test import APIClient

from mneia_backend.models.work_type import WorkType


@pytest.mark.django_db
def test_work_type_str():
    work_type = WorkType.objects.get(id="66b8026e-7ce8-36f8-a8d5-7c346c7b9a88")  # from fixture
    assert str(work_type) == "Poem"


@pytest.mark.django_db
def test_work_type_import_from_musicbrainz_new_work_type():
    """
    Test that when trying to import a new Area Type that does not already exist, the new Area Type is returned.
    """
    api_client = APIClient()

    response = api_client.get("/work-types/f061270a-2fd6-32f1-a641-f0f8676d14e6/")
    assert response.status_code == 404  # assert that the WorkType "Song" does not already exist before we import it

    response = api_client.post("/work-types/import/", data={"mbid": 17})
    assert response.status_code == 200  # import succeeded

    response = api_client.get("/work-types/f061270a-2fd6-32f1-a641-f0f8676d14e6/")
    assert response.status_code == 200  # the WorkType exists after we import it

    # Now test importing a WorkType that has a parent:
    response = api_client.post("/work-types/import/", data={"mbid": 10000})
    assert response.data["parent"] == uuid.UUID("f061270a-2fd6-32f1-a641-f0f8676d14e6")
