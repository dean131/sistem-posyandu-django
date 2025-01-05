from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .serializers import (
    ChildSerializer,
    PosyanduActivitySerializer,
)
from village.models import Village
from posyandu.models import Posyandu

from posyanduapp.utils.custom_responses.custom_response import CustomResponse

from posyandu_activity.models import PosyanduActivity


class PosyanduActivityViewSet(ModelViewSet):
    serializer_class = PosyanduActivitySerializer
    queryset = PosyanduActivity.objects.all()

    def get_queryset(self):
        user = self.request.user

        # Filter activities based on the user's role
        if user.role == "CADRE":
            # Cadre is related to Posyandu via the cadres field
            posyandus = Posyandu.objects.filter(cadres=user)
        elif user.role == "MIDWIFE":
            # Midwife is related to villages, which are related to Posyandu
            villages = Village.objects.filter(midwifes=user)
            posyandus = Posyandu.objects.filter(village__in=villages)
        elif user.role == "PARENT":
            # Parent is related to Posyandu via the parents field
            posyandus = Posyandu.objects.filter(parents=user)
        else:
            # For other roles, return no activities
            posyandus = Posyandu.objects.none()

        # Return activities related to the filtered Posyandu(s)
        return PosyanduActivity.objects.filter(posyandu__in=posyandus)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.retrieve(
            "PosyanduActivity berhasil ditemukan", serializer.data
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by("-date")
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Cek apakah posyandu activity sudah ada
        is_exists = PosyanduActivity.objects.filter(
            date=request.data["date"], posyandu=request.data["posyandu"]
        ).exists()
        if is_exists:
            return CustomResponse.bad_request(
                "Sudah ada aktivitas posyandu pada tanggal tersebut"
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("PosyanduActivity berhasil ditambahkan")
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

            return CustomResponse.ok("PosyanduActivity berhasil diubah")
        return CustomResponse.serializers_erros(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.ok("PosyanduActivity berhasil dihapus")

    @action(detail=False, methods=["get"])
    def active(self, request, *args, **kwargs):
        """
        Returns active Posyandu activities for today based on the user's role.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Filter activities happening today in the retrieved Posyandu(s)
        today = timezone.now().date()
        queryset = queryset.filter(date=today).order_by("-date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.list(serializer.data)

    @action(detail=True, methods=["get"])
    def children(self, request, *args, **kwargs):
        """
        mengembalikan data anak yang ada di posyandu activity tertentu
        """
        instance = self.get_object()

        # get data anak yang sudah di ukur
        child_measured_ids = instance.childmeasurement_set.all().values_list(
            "child", flat=True
        )

        print(child_measured_ids)

        # Get data anak berdasarkan PosyanduActivity
        children = []
        parent_posyandus = instance.posyandu.parentposyandu_set.all()
        for parent_posyandu in parent_posyandus:
            children.extend(parent_posyandu.parent.child_set.all())

        # Tambahan context untuk serializer
        context = self.get_serializer_context()
        context["child_measured_ids"] = child_measured_ids

        page = self.paginate_queryset(children)
        if page is not None:
            serializer = ChildSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = ChildSerializer(children, many=True, context=context)
        return CustomResponse.list(serializer.data)
