from django.urls import path
from . import views

urlpatterns = [
    path("village_list/", views.VillageListView.as_view(), name="village_list"),
    path("village_create/", views.VillageCreateView.as_view(), name="village_create"),
    path(
        "village_update/<str:pk>/",
        views.VillageUpdateView.as_view(),
        name="village_update",
    ),
    path(
        "village_delete/<str:pk>/",
        views.VillageDeleteView.as_view(),
        name="village_delete",
    ),
]
