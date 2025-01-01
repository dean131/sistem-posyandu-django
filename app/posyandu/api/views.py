"""
Posyandu Views
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from posyandu.api.serializers import ChildSerializer, PosyanduSerializer

from posyanduapp.utils.custom_responses.custom_response import CustomResponse

from posyandu.models import Posyandu
from child.models import Child


class PosyanduViewSet(ModelViewSet):
    serializer_class = PosyanduSerializer
    queryset = Posyandu.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.list(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve("Posyandu berhasil ditemukan", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("Posyandu berhasil ditambahkan")
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

            return CustomResponse.ok("Posyandu berhasil diubah")
        return CustomResponse.serializers_erros(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("Posyandu berhasil dihapus")

    @action(detail=False, methods=["get"])
    def by_user_role(self, request, *args, **kwargs):
        if request.user.role == "MIDWIFE":
            midwifeassignments = request.user.midwifeassignment_set.all()
            villages = [
                midwifeassignment.village for midwifeassignment in midwifeassignments
            ]
            queryset = [
                posyandu
                for village in villages
                for posyandu in village.posyandu_set.all()
            ]
        elif request.user.role == "CADRE":
            queryset = [
                assignment.posyandu
                for assignment in request.user.cadreassignment_set.all()
            ]
        elif request.user.role == "PARENT":
            queryset = [
                parentposyandu.posyadu
                for parentposyandu in request.user.parentposyandu_set.all()
            ]
        else:
            return CustomResponse.bad_request("Role user tidak valid")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.list(serializer.data)

    @action(detail=True, methods=["get"])
    def children(self, request, *args, **kwargs):
        instance = self.get_object()

        queryset = Child.objects.filter(parent__parentposyandu__posyandu=instance)

        context = self.get_serializer_context()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ChildSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = ChildSerializer(queryset, many=True, context=context)
        return CustomResponse.list(serializer.data)
