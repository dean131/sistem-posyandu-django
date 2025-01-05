from django.urls import path, include

from rest_framework.routers import DefaultRouter

from posyandu.api.views import PosyanduViewSet


router = DefaultRouter()

router.register(r"posyandu", PosyanduViewSet, basename="posyandu")

urlpatterns = [
    path("", include(router.urls)),
]
