from rest_framework.viewsets import ModelViewSet

from .serializers import ChildMeasurementSerializer

from posyanduapp.utils.custom_response import CustomResponse

from base.models import ChildMeasurement


class ChildMeasurementViewSet(ModelViewSet):
    serializer_class = ChildMeasurementSerializer
    queryset = ChildMeasurement.objects.all()
    filterset_fields = ['child', 'posyandu_activity']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()).order_by('-age_in_month')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.list(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve(
            "ChildMeasurement berhasil ditemukan",
            serializer.data
        )

    def create(self, request, *args, **kwargs):
        child_id = request.data.get('child')
        posyandu_activity_id = request.data.get('posyandu_activity')

        # Cek apakah child sudah diukur
        posyandu_activity = ChildMeasurement.objects.filter(
            child=child_id,
            posyandu_activity=posyandu_activity_id
        )

        # jika sudah diukur, maka update data
        if posyandu_activity.exists():
            serializer = self.get_serializer(
                posyandu_activity.first(), data=request.data)
            if serializer.is_valid():
                self.perform_update(serializer)
                return CustomResponse.ok("ChildMeasurement berhasil diubah")
            return CustomResponse.serializers_erros(serializer.errors)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("ChildMeasurement berhasil ditambahkan")
        return CustomResponse.serializers_erros(serializer.errors)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return CustomResponse.ok("ChildMeasurement berhasil diubah")
        return CustomResponse.serializers_erros(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("ChildMeasurement berhasil dihapus")
