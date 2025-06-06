import pytest

from mneia_backend.models.link_attribute_text_value import LinkAttributeTextValue


@pytest.mark.django_db
def test_link_attribute_text_value_attribute_type_name():
    link_attribute_text_value = LinkAttributeTextValue.objects.get(id="a6dfb38e-9fca-4b53-b8a8-488043525feb")
    assert link_attribute_text_value.attribute_type_name == "page"
