from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api.views import (
    village,
    midwife_assignment,
    cadre_assignment,
    parent_posyandu,
)
from base.api.views.posyandu.views import PosyanduViewSet
from base.api.views.posyandu_activity.views import PosyanduActivityViewSet
from base.api.views.child.views import ChildViewSet
from base.api.views.childmeasuremnet.views import ChildMeasurementViewSet


router = DefaultRouter()
router.register(r'children', ChildViewSet, basename='child')
router.register(r'villages', village.VillageViewSet, basename='village')
router.register(r'posyandu', PosyanduViewSet, basename='posyandu')
router.register(r'midwifeassignments',
                midwife_assignment.MidwifeAssignmentViewSet, basename='midwifeassignment')
router.register(r'cadreassignments',
                cadre_assignment.CadreAssignmentViewSet, basename='cadreassignment')
router.register(r'posyanduactivities', PosyanduActivityViewSet,
                basename='posyanduactivity')
router.register(r'childmeasurements', ChildMeasurementViewSet,
                basename='childmeasurement')
router.register(r'parentposyandu',
                parent_posyandu.ParentPosyanduViewSet, basename='parentposyandu')


urlpatterns = [
    path('', include(router.urls)),
]
