from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api.views import (
    village,
    posyandu,
    midwife_assignment,
    cadre_assignment,
)


router = DefaultRouter()
router.register(r'villages', village.VillageViewSet, basename='village')
router.register(r'posyandu', posyandu.PosyanduViewSet, basename='posyandu')
router.register(r'midwifeassignments', midwife_assignment.MidwifeAssignmentViewSet, basename='midwifeassignment')
router.register(r'cadreassignments', cadre_assignment.CadreAssignmentViewSet, basename='cadreassignment')

urlpatterns = [
    path('', include(router.urls)),
]