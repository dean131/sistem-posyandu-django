"""
Child Views
"""

from multiprocessing import context
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from child.api.serializers import (
    ChildInfoSerializer,
    ChildSerializer,
    GrowthChartSerializer,
    ChildMeasurementSerializer,
)

from posyanduapp.utils.custom_responses.custom_response import CustomResponse

from child.models import Child


class ChildViewSet(ModelViewSet):
    serializer_class = ChildSerializer
    queryset = Child.objects.all()

    def get_serializer_class(self):
        if self.action == "info":
            return ChildInfoSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve("Child berhasil ditemukan", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("Child berhasil ditambahkan")
        return CustomResponse.serializers_erros(serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return CustomResponse.ok("Child berhasil diubah")
        return CustomResponse.serializers_erros(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("Child berhasil dihapus")

    @action(detail=True, methods=["get"])
    def info(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve("Child berhasil ditemukan", serializer.data)

    @action(detail=True, methods=["get"])
    def growth_chart(self, request, *args, **kwargs):
        instance = self.get_object()
        context = self.get_serializer_context()
        serializer = GrowthChartSerializer(instance.growthchart, context=context)
        return CustomResponse.retrieve(
            "Growth Chart berhasil ditemukan", serializer.data
        )

    # @action(detail=False, methods=["get"])
    # def by_user_role(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     # Get child based on role user

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return CustomResponse.list(serializer.data)
