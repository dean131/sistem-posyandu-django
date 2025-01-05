from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("midwife_list/", views.MidwifeListView.as_view(), name="midwife_list"),
    path(
        "assign_village/<str:pk>/",
        views.AssignVillageToMidwifeView.as_view(),
        name="assign_village_to_midwife",
    ),
    path("cadre_list/", views.CadreListView.as_view(), name="cadre_list"),
    path(
        "assign_posyandu_to_cadre/<str:pk>/",
        views.AssignPosyanduToCadreView.as_view(),
        name="assign_posyandu_to_cadre",
    ),
]
