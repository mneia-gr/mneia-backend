from django.urls import include, path
from rest_framework import routers

from mneia_backend.models.area import AreaViewSet
from mneia_backend.models.area_type import AreaTypeViewSet

mneia_router = routers.DefaultRouter()
mneia_router.register(r"areas", AreaViewSet)
mneia_router.register(r"area-types", AreaTypeViewSet)

urlpatterns = [
    path("", include(mneia_router.urls)),
]
