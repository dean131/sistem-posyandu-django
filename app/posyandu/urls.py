from django.urls import path

from posyandu import views

urlpatterns = [
    path("posyandu_list/", views.PosyanduListView.as_view(), name="posyandu_list"),
    path(
        "posyandu_create/", views.PosyanduCreateView.as_view(), name="posyandu_create"
    ),
    path(
        "posyandu_update/<str:pk>/",
        views.PosyanduUpdateView.as_view(),
        name="posyandu_update",
    ),
    path(
        "posyandu_delete/<str:pk>/",
        views.PosyanduDeleteView.as_view(),
        name="posyandu_delete",
    ),
]
