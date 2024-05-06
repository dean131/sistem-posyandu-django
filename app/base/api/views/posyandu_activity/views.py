from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from base.api.views.posyandu_activity.serializers import PosyanduActivitySerializer

from posyanduapp.utils.custom_response import CustomResponse

from base.models import CadreAssignment, PosyanduActivity


class PosyanduActivityViewSet(ModelViewSet):
    serializer_class = PosyanduActivitySerializer
    queryset = PosyanduActivity.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve(
            "PosyanduActivity berhasil ditemukan",
            serializer.data
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("PosyanduActivity berhasil ditambahkan")
        return CustomResponse.serializers_erros(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            
            return CustomResponse.ok("PosyanduActivity berhasil diubah")
        return CustomResponse.serializers_erros(serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("PosyanduActivity berhasil dihapus")
    
    @action(detail=False, methods=['get'])
    def active(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get posyandu berdasarkan role user
        if request.user.role == "CADRE":
            posyandus = request.user.cadreassignment_set.all().values('posyandu')
        elif request.user.role == "MIDWIFE":
            posyandus = request.user.midwifeassignment_set.all().values('posyandu')
        elif request.user.role == "PARENT":
            posyandus = request.user.parentposyandu_set.all().values('posyandu')
        elif request.user.role == "PUSKESMAS":
            posyandus = request.user.puskesmasassignment_set.all().values('posyandu')
        else:
            posyandus = []

        today = timezone.now().date()
        queryset = queryset.filter(date=today, posyandu__in=posyandus)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.list(serializer.data)

    