from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posyandu_activity.api.views import PosyanduActivityViewSet

router = DefaultRouter()

router.register(
    r"posyanduactivities", PosyanduActivityViewSet, basename="posyanduactivity"
)

urlpatterns = [
    path("", include(router.urls)),
]
