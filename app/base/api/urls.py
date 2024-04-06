from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api.views import (
    village,
    posyandu,
    midwifeassignment
)


router = DefaultRouter()
router.register(r'villages', village.VillageViewSet, basename='village')
router.register(r'posyandu', posyandu.PosyanduViewSet, basename='posyandu')
router.register(r'midwifeassignments', midwifeassignment.MidwifeAssignmentViewSet, basename='midwifeassignment')


urlpatterns = [
    path('', include(router.urls)),
]