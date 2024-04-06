from rest_framework.viewsets import ModelViewSet

from base.api.serializers.posyandu import PosyanduSerializer

from posyanduapp.utils.custom_response import CustomResponse

from base.models import Posyandu


class PosyanduViewSet(ModelViewSet):
    serializer_class = PosyanduSerializer
    queryset = Posyandu.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve(
            "Posyandu berhasil ditemukan",
            serializer.data
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("Posyandu berhasil ditambahkan")
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
            
            return CustomResponse.ok("Posyandu berhasil diubah")
        return CustomResponse.serializers_erros(serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("Posyandu berhasil dihapus")
    