from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api.views import child
from base.api.views import (
    village,
    posyandu,
    midwife_assignment,
    cadre_assignment,
    posyandu_activity,
    child_measurement,
)


router = DefaultRouter()
router.register(r'villages', village.VillageViewSet, basename='village')
router.register(r'posyandu', posyandu.PosyanduViewSet, basename='posyandu')
router.register(r'midwifeassignments', midwife_assignment.MidwifeAssignmentViewSet, basename='midwifeassignment')
router.register(r'cadreassignments', cadre_assignment.CadreAssignmentViewSet, basename='cadreassignment')
router.register(r'posyanduactivities', posyandu_activity.PosyanduActivityViewSet, basename='posyanduactivity')
router.register(r'children', child.ChildViewSet, basename='child')
router.register(r'childmeasurements', child_measurement.ChildMeasurementViewSet, basename='childmeasurement')

urlpatterns = [
    path('', include(router.urls)),
]