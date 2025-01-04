from django.urls import path
from . import views

urlpatterns = [
    path(
        "posyandu_activity/",
        views.PosyanduActivityListView.as_view(),
        name="posyandu_activity_list",
    ),
    path(
        "posyandu_activity/<str:pk>/",
        views.PosyanduActivityDetailView.as_view(),
        name="posyandu_activity_detail",
    ),
    path(
        "activities/<str:pk>/export_measurements/",
        views.export_child_measurements_to_excel,
        name="export_child_measurements",
    ),
]
