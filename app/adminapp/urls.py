from django.urls import path

from adminapp import views


urlpatterns = [    
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('village_list/', views.VillageListView.as_view(), name='village_list'),
    path('posyandu/', views.PosyanduView.as_view(), name='posyandu'),
]