from django.urls import path, include

from adminapp import views


urlpatterns = [    
    path('', views.dashboard, name='dashboard'),
]