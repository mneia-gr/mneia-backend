from django.urls import include, path
from rest_framework import routers

from mneia_backend.models.area import AreaViewSet
from mneia_backend.models.area_type import AreaTypeViewSet
from mneia_backend.models.gender import GenderViewSet

mneia_router = routers.DefaultRouter()
mneia_router.register(r"areas", AreaViewSet)
mneia_router.register(r"area-types", AreaTypeViewSet)
mneia_router.register(r"genders", GenderViewSet)

urlpatterns = [
    path("", include(mneia_router.urls)),
]
