from django.contrib.auth import authenticate, login
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from account.api.serializers import (
    UserSerializer,
    ParentSerializer,
    MidwifeSerializer,
    CadreSerializer,
    PuskesmasSerializer,
)
from account.models import (
    User,
    Parent,
    Midwife,
    Cadre,
    Puskesmas,
)
from child.api.serializers import ChildSerializer
from child.models import Child
from posyanduapp.utils.custom_responses.custom_response import CustomResponse


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        methods = [
            "login_password",
            "login_otp",
            "login_otp_validate",
            "register_otp_validate",
            "create",
        ]
        if self.action in methods:
            return [
                AllowAny(),
            ]
        return super().get_permissions()

    @action(detail=False, methods=["get"])
    def current(self, request):
        user = request.user
        if user is None:
            return CustomResponse.unauthorized("Anda belum login")
        serializer = self.get_serializer(user)
        return CustomResponse.retrieve(
            message="Data pengguna berhasil ditemukan", data=serializer.data
        )

    def create(self, request, *args, **kwargs):
        whatsapp = request.data.get("whatsapp")
        user = User.objects.filter(whatsapp=whatsapp, is_active=False).first()
        if user is not None:
            # Jika user registrasi dengan nomor whatsapp yang sama
            # tapi belum menyelesaikan proses registrasi.
            # Maka akan dikirimkan ulang kode OTP
            user.delete()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.send_otp_wa()
            return CustomResponse.ok("Berhasil menambahkan data")
        return CustomResponse.serializers_erros(serializer.errors)

    @action(detail=False, methods=["post"])
    def login_otp(self, request):
        whatsapp = request.data.get("whatsapp")

        if not whatsapp:
            return CustomResponse.bad_request("Silahkan masukkan nomor whatsapp Anda")

        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return CustomResponse.bad_request("Pengguna tidak ditemukan")

        if user.is_active is False:
            return CustomResponse.bad_request("Nomor whatsapp belum terdaftar")

        user.send_otp_wa()
        return CustomResponse.ok("OTP telah dikirim ke nomor whatsapp Anda")

    @action(detail=False, methods=["post"])
    def login_otp_validate(self, request):
        whatsapp = request.data.get("whatsapp")
        otp_code = request.data.get("otp_code")

        if not whatsapp or not otp_code:
            return CustomResponse.bad_request(
                "Silahkan masukkan nomor whatsapp dan kode OTP"
            )

        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return CustomResponse.bad_request("Akun tidak ditemukan")

        if user.is_active is False:
            return CustomResponse.bad_request("Akun belum terdaftar")

        if not user.otp.validate_otp(otp_code):
            return CustomResponse.bad_request("OTP tidak valid atau sudah kadaluarsa")

        jwt_token = RefreshToken.for_user(user)
        jwt_token["role"] = user.role
        return CustomResponse.jwt(jwt_token)

    @action(detail=False, methods=["post"])
    def register_otp_validate(self, request):
        whatsapp = request.data.get("whatsapp")
        otp_code = request.data.get("otp_code")

        if not whatsapp or not otp_code:
            return CustomResponse.bad_request(
                "Silahkan masukkan nomor whatsapp dan kode OTP"
            )

        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return CustomResponse.bad_request(
                "Nomor Whatsapp yang Anda masukkan tidak salah"
            )

        if user.is_active:
            return CustomResponse.bad_request("Whatsapp sudah terdaftar")

        if not user.otp.validate_otp(otp_code):
            return CustomResponse.bad_request("OTP tidak valid atau sudah kadaluarsa")

        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        return CustomResponse.jwt(refresh)


class ParentViewSet(UserViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    @action(detail=True, methods=["get"])
    def children(self, request, pk=None):
        """
        Retrieve all children associated with a specific parent.
        """
        parent = self.get_object()
        children = Child.objects.filter(parent=parent)
        context = self.get_serializer_context()

        page = self.paginate_queryset(children)
        if page is not None:
            serializer = ChildSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        # Serialize and return the children data
        serializer = ChildSerializer(children, many=True)
        return CustomResponse.list(serializer.data)


class MidwifeViewSet(UserViewSet):
    queryset = Midwife.objects.all()
    serializer_class = MidwifeSerializer


class CadreViewSet(UserViewSet):
    queryset = Cadre.objects.all()
    serializer_class = CadreSerializer


class PuskesmasViewSet(UserViewSet):
    queryset = Puskesmas.objects.all()
    serializer_class = PuskesmasSerializer
