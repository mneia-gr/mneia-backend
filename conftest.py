import pytest
from django.apps import apps
from django.core.management import call_command
from django_musicbrainz_connector.apps import DjangoMusicbrainzConnectorConfig


def _convert_unmanaged_models_to_managed():
    """
    Our dependency app "Django MusicBrainz Connector" has unmanaged models, because it connects to an existing replica
    the MusicBrainz database. Here we are converting the unmanaged models to managed models during testing, so that we
    can load test fixtures and test importing data from MusicBrainz into Mneia.
    """
    unmanaged_models = [
        model
        for model in apps.get_app_config(DjangoMusicbrainzConnectorConfig.name).get_models()
        if model._meta.managed is False
    ]
    for model in unmanaged_models:
        print(f"MNEIA-BACKEND TESTS: Converting unmanaged Django MusicBrainz Connector model '{model}' to managed")
        model._meta.managed = True


def _load_test_fixtures(django_db_blocker):
    """
    Loads all JSON fixtures. Some of these fixtures have to be loaded in order, because they have dependencies on each
    other.
    """
    fixtures = [
        "area-type",
        "area",  # depends on area-type
        "gender",
    ]
    with django_db_blocker.unblock():
        for fixture in fixtures:
            print(f"MNEIA-BACKEND TESTS: Loading fixture {fixture}.json...")
            call_command("loaddata", f"mneia_backend/tests/fixtures/{fixture}.json")


@pytest.mark.django_db
def pytest_sessionstart():
    print("MNEIA-BACKEND TESTS: pytest_sessionstart")
    _convert_unmanaged_models_to_managed()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    _load_test_fixtures(django_db_blocker)
