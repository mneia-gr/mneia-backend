from django.urls import include, path
from rest_framework import routers

from mneia_backend.models.area import AreaViewSet
from mneia_backend.models.area_type import AreaTypeViewSet
from mneia_backend.models.gender import GenderViewSet
from mneia_backend.models.link_type import LinkTypeViewSet
from mneia_backend.models.person import PersonViewSet

mneia_router = routers.DefaultRouter()
mneia_router.register(r"areas", AreaViewSet)
mneia_router.register(r"area-types", AreaTypeViewSet)
mneia_router.register(r"genders", GenderViewSet)
mneia_router.register(r"link-types", LinkTypeViewSet)
mneia_router.register(r"people", PersonViewSet)

urlpatterns = [
    path("", include(mneia_router.urls)),
]
