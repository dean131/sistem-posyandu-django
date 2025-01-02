"""
Posyandu Views
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from posyandu.api.serializers import ChildSerializer, PosyanduSerializer

from posyanduapp.utils.custom_responses.custom_response import CustomResponse

from posyandu.models import Posyandu
from child.models import Child
from village.models import Village


class PosyanduViewSet(ModelViewSet):
    serializer_class = PosyanduSerializer
    queryset = Posyandu.objects.all()


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from posyandu.models import Posyandu, Village
from .serializers import PosyanduSerializer


class PosyanduViewSet(ModelViewSet):
    serializer_class = PosyanduSerializer
    queryset = Posyandu.objects.all()

    def list(self, request, *args, **kwargs):
        """
        List Posyandu data filtered by the user's role and relationships.
        """
        user = request.user

        # Filter Posyandu based on the user's role
        if user.role == "CADRE":
            queryset = Posyandu.objects.filter(cadres=user)
        elif user.role == "MIDWIFE":
            villages = Village.objects.filter(midwifes=user)
            queryset = Posyandu.objects.filter(village__in=villages)
        elif user.role == "PARENT":
            queryset = Posyandu.objects.filter(parents=user)
        else:
            queryset = Posyandu.objects.none()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
