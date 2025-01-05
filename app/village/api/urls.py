from django.urls import path, include

from rest_framework.routers import DefaultRouter

from village.api.views import VillageViewSet


router = DefaultRouter()

router.register(r"villages", VillageViewSet, basename="village")

urlpatterns = [
    path("", include(router.urls)),
]
