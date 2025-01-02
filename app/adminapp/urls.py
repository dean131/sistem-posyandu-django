from django.urls import path

from adminapp import views


urlpatterns = [
    # path(
    #     "posyandu_activities/",
    #     views.PosyanduActivitiesView.as_view(),
    #     name="posyandu_activities",
    # ),
    path(
        "village_info/<str:pk>/", views.VillageInfoView.as_view(), name="village_info"
    ),
    # path("midwives/", views.MidwifeView.as_view(), name="midwives"),
    path(
        "midwife_info/<str:pk>/", views.MidwifeInfoView.as_view(), name="midwife_info"
    ),
    path(
        "midwife_assignments/",
        views.MidwifeAssignmentView.as_view(),
        name="midwife_assignments",
    ),
    # path("cadres/", views.CadreView.as_view(), name="cadres"),
    path("parents/", views.ParentView.as_view(), name="parents"),
    # path("children/", views.ChildView.as_view(), name="children"),
    # path("length_for_age_boys/", views.LengthForAgeBoysView.as_view(), name="length_for_age_boys"),
    # path("length_for_age_girls/", views.LengthForAgeGirlsView.as_view(), name="length_for_age_girls"),
    # path("height_for_age_boys/", views.HeightForAgeBoysView.as_view(), name="height_for_age_boys"),
    # path("height_for_age_girls/", views.HeightForAgeGirlsView.as_view(), name="height_for_age_girls"),
    # path("weight_for_age_boys/", views.WeightForAgeBoysView.as_view(), name="weight_for_age_boys"),
    # path("weight_for_age_girls/", views.WeightForAgeGirlsView.as_view(), name="weight_for_age_girls"),
]
