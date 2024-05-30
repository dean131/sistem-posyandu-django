from django.urls import path

from adminapp import views


urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    path("posyandu_activities/", views.PosyanduActivitiesView.as_view(),
         name="posyandu_activities"),

    path("village_list/", views.VillageListView.as_view(), name="village_list"),
    path("village_info/<str:pk>/",
         views.VillageInfoView.as_view(), name="village_info"),

    path("posyandu/", views.PosyanduView.as_view(), name="posyandu"),

    path("midwives/", views.MidwifeView.as_view(), name="midwives"),
    path("midwife_info/<str:pk>/",
         views.MidwifeInfoView.as_view(), name="midwife_info"),

    path("midwife_assignments/", views.MidwifeAssignmentView.as_view(),
         name="midwife_assignments"),

    path("parents/", views.ParentView.as_view(), name="parents"),

    path("children/", views.ChildView.as_view(), name="children"),

    path("anthropometric_standard/", views.AnthropometricStandardView.as_view(),
         name="anthropometric_standard"),

    # path("length_for_age_boys/", views.LengthForAgeBoysView.as_view(), name="length_for_age_boys"),
    # path("length_for_age_girls/", views.LengthForAgeGirlsView.as_view(), name="length_for_age_girls"),

    # path("height_for_age_boys/", views.HeightForAgeBoysView.as_view(), name="height_for_age_boys"),
    # path("height_for_age_girls/", views.HeightForAgeGirlsView.as_view(), name="height_for_age_girls"),

    # path("weight_for_age_boys/", views.WeightForAgeBoysView.as_view(), name="weight_for_age_boys"),
    # path("weight_for_age_girls/", views.WeightForAgeGirlsView.as_view(), name="weight_for_age_girls"),
]
