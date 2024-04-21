from django.urls import path

from adminapp import views


urlpatterns = [    
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    path("village_list/", views.VillageListView.as_view(), name="village_list"),
    path("village_info/<str:pk>/", views.VillageInfoView.as_view(), name="village_info"),
    
    path("posyandu/", views.PosyanduView.as_view(), name="posyandu"),

    path("midwives/", views.MidwifeView.as_view(), name="midwives"),
    path("midwife_info/<str:pk>/", views.MidwifeInfoView.as_view(), name="midwife_info"),
]