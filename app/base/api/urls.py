from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api.views.village import (
    VillageViewSet,
)


router = DefaultRouter()
router.register(r'villages', VillageViewSet, basename='village')

urlpatterns = [
    path('', include(router.urls)),
]