from rest_framework.viewsets import ModelViewSet

from base.api.serializers.midwifeassignment import MidwifeAssignmentSerializer

from posyanduapp.utils.custom_response import CustomResponse

from base.models import MidwifeAssignment


class MidwifeAssignmentViewSet(ModelViewSet):
    serializer_class = MidwifeAssignmentSerializer
    queryset = MidwifeAssignment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve(
            "MidwifeAssignment berhasil ditemukan",
            serializer.data
        )

    def create(self, request, *args, **kwargs):
        midwife = request.data.get('midwife')
        village = request.data.get('village')

        # Cek apakah midwife sudah ada di desa tersebut
        if MidwifeAssignment.objects.filter(midwife=midwife, village=village).exists():
            return CustomResponse.bad_request("MidwifeAssignment sudah ada")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("MidwifeAssignment berhasil ditambahkan")
        return CustomResponse.serializers_erros(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("MidwifeAssignment berhasil dihapus")
    
    def update(self, request, *args, **kwargs):
        return CustomResponse.bad_request("Tidak bisa mengubah MidwifeAssignment")
     