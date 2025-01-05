from django.urls import path, include
from child.api.views import ChildViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"children", ChildViewSet, basename="child")

urlpatterns = [
    path("", include(router.urls)),
]
