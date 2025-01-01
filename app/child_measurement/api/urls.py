from django.urls import path, include
from child_measurement.api.views import ChildMeasurementViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(
    r"childmeasurements", ChildMeasurementViewSet, basename="childmeasurement"
)

urlpatterns = [
    path("", include(router.urls)),
]
