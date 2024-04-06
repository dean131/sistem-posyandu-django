from django.urls import path, include

from rest_framework.routers import DefaultRouter

from account.api.views import (
    UserViewSet,
    ParentViewSet,
    MidwifeViewSet,
    CadreViewSet,
    PuskesmasViewSet,
)


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'parents', ParentViewSet, basename='parent')
router.register(r'midwives', MidwifeViewSet, basename='midwife')
router.register(r'cadres', CadreViewSet, basename='cadre')
router.register(r'puskesmas', PuskesmasViewSet, basename='puskesmas')

urlpatterns = [
    path('', include(router.urls)),
]