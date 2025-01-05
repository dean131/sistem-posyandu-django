from django.urls import path
from . import views

urlpatterns = [
    path(
        "posyandu_activity/<str:activity_id>/measurements/",
        views.ChildMeasurementListView.as_view(),
        name="child_measurement_list",
    ),
    path(
        "anthropometric_standard/",
        views.AnthropometricStandardView.as_view(),
        name="anthropometric_standard",
    ),
]
