from django.urls import include, path
from rest_framework import routers

from mneia_backend.models.area import AreaViewSet
from mneia_backend.models.area_type import AreaTypeViewSet
from mneia_backend.models.gender import GenderViewSet
from mneia_backend.models.link import LinkViewSet
from mneia_backend.models.link_attribute import LinkAttributeViewSet
from mneia_backend.models.link_attribute_type import LinkAttributeTypeViewSet
from mneia_backend.models.link_type import LinkTypeViewSet
from mneia_backend.models.person import PersonViewSet
from mneia_backend.models.work import WorkViewSet
from mneia_backend.models.work_type import WorkTypeViewSet

mneia_router = routers.DefaultRouter()
mneia_router.register(r"areas", AreaViewSet)
mneia_router.register(r"area-types", AreaTypeViewSet)
mneia_router.register(r"genders", GenderViewSet)
mneia_router.register(r"link-types", LinkTypeViewSet)
mneia_router.register(r"link-attributes", LinkAttributeViewSet)
mneia_router.register(r"link-attribute-types", LinkAttributeTypeViewSet)
mneia_router.register(r"links", LinkViewSet)
mneia_router.register(r"people", PersonViewSet)
mneia_router.register(r"work-types", WorkTypeViewSet)
mneia_router.register(r"works", WorkViewSet)

urlpatterns = [
    path("", include(mneia_router.urls)),
]
