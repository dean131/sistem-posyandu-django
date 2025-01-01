from rest_framework.viewsets import ModelViewSet

from base.api.serializers.parent_posyandu import ParentPosyanduSerializer

from posyanduapp.utils.custom_responses.custom_response import CustomResponse

from base.models import ParentPosyandu


class ParentPosyanduViewSet(ModelViewSet):
    serializer_class = ParentPosyanduSerializer
    queryset = ParentPosyandu.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve(
            "ParentPosyandu berhasil ditemukan", serializer.data
        )

    def create(self, request, *args, **kwargs):
        parent = request.data.get("parent")
        posyandu = request.data.get("posyandu")

        # Cek apakah parent sudah ada di posyandu tersebut
        if ParentPosyandu.objects.filter(parent=parent, posyandu=posyandu).exists():
            return CustomResponse.bad_request("ParentPosyandu sudah ada")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("ParentPosyandu berhasil ditambahkan")
        return CustomResponse.serializers_erros(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("ParentPosyandu berhasil dihapus")

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

            return CustomResponse.ok("ParentPosyandu berhasil diubah")
        return CustomResponse.serializers_erros(serializer.errors)
