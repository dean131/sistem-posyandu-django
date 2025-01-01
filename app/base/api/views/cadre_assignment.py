from rest_framework.viewsets import ModelViewSet

from base.api.serializers.cadre_assignment import CadreAssignmentSerializer

from posyanduapp.utils.custom_responses.custom_response import CustomResponse

from base.models import CadreAssignment


class CadreAssignmentViewSet(ModelViewSet):
    serializer_class = CadreAssignmentSerializer
    queryset = CadreAssignment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve(
            "CadreAssignment berhasil ditemukan", serializer.data
        )

    def create(self, request, *args, **kwargs):
        cadre = request.data.get("cadre")
        posyandu = request.data.get("posyandu")

        # Cek apakah cadre sudah ada di posyandu tersebut
        if CadreAssignment.objects.filter(cadre=cadre, posyandu=posyandu).exists():
            return CustomResponse.bad_request(
                "Kader sudah ditambahkan di posyandu lain"
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("CadreAssignment berhasil ditambahkan")
        return CustomResponse.serializers_erros(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("CadreAssignment berhasil dihapus")

    def update(self, request, *args, **kwargs):
        return CustomResponse.bad_request("Tidak bisa mengubah CadreAssignment")
