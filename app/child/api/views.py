"""
Child Views
"""

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from child.api.serializers import ChildInfoSerializer, ChildSerializer

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

    @action(detail=False, methods=["get"])
    def by_user_role(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get child berdasarkan role user
        if request.user.role == "PARENT":
            queryset = self.queryset.filter(parent=request.user)
        else:
            if request.user.role == "CADRE":
                posyandus = request.user.cadreassignment_set.all().values("posyandu")
            elif request.user.role == "MIDWIFE":
                midwifeassignments = request.user.midwifeassignment_set.all()
                villages = [
                    midwifeassignment.village
                    for midwifeassignment in midwifeassignments
                ]
                posyandus = [
                    posyandu
                    for village in villages
                    for posyandu in village.posyandu_set.all()
                ]
            queryset = queryset.filter(parent__parentposyandu__posyandu__in=posyandus)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
