from django.urls import path
from . import views

urlpatterns = [
    path("child_list/", views.ChildListView.as_view(), name="child_list"),
    path(
        "child_detail/<str:pk>/", views.ChildDetailView.as_view(), name="child_detail"
    ),
]
