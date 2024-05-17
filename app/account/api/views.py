from django.contrib.auth import authenticate, login

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken

from account.api.serializers import (
    UserSerializer,

    ParentSerializer,
    ParentRegistrationSerializer,

    MidwifeSerializer,
    MidwifeRegistrationSerializer,

    CadreSerializer,
    CadreRegistrationSerializer,

    PuskesmasSerializer,
    PuskesmasRegistrationSerializer,
)

from account.models import (
    User,
    Parent,
    Midwife,
    Cadre,
    Puskesmas,
)

from posyanduapp.utils.custom_response import CustomResponse


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser,]

    def get_permissions(self):
        if self.action in [
            "login_password",
            "login_otp",
            "login_otp_validate",
                "register_otp_validate"]:
            return [AllowAny(),]
        return super().get_permissions()

    @action(detail=False, methods=["post"])
    def login_password(self, request):
        whatsapp = request.data.get("whatsapp")
        password = request.data.get("password")

        if not whatsapp or not password:
            return CustomResponse.bad_request("Silahkan masukkan nomor whatsapp dan password")

        user = authenticate(request, whatsapp=whatsapp, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            refresh["role"] = user.role
            return CustomResponse.jwt(refresh)
        else:
            return CustomResponse.bad_request("Kredential tidak valid")

    @action(detail=False, methods=["post"])
    def login_otp(self, request):
        whatsapp = request.data.get("whatsapp")

        if not whatsapp:
            return CustomResponse.bad_request("Silahkan masukkan nomor whatsapp Anda")

        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return CustomResponse.bad_request("Pengguna tidak ditemukan")

        if not user.is_registered:
            return CustomResponse.bad_request("Nomor whatsapp belum terdaftar")

        user.otp.send_otp_wa()
        return CustomResponse.ok("OTP telah dikirim ke nomor whatsapp Anda")

    @action(detail=False, methods=["post"])
    def login_otp_validate(self, request):
        whatsapp = request.data.get("whatsapp")
        otp_code = request.data.get("otp_code")

        if not whatsapp or not otp_code:
            return CustomResponse.bad_request("Silahkan masukkan nomor whatsapp dan kode OTP")

        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return CustomResponse.bad_request("Akun tidak ditemukan")

        if not user.is_registered:
            return CustomResponse.bad_request("Akun belum terdaftar")

        if not user.otp.validate_otp(otp_code):
            return CustomResponse.bad_request("OTP tidak valid atau sudah kadaluarsa")

        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        refresh["user"] = UserSerializer(user).data
        return CustomResponse.jwt(refresh)

    @action(detail=False, methods=["post"])
    def register_otp_validate(self, request):
        whatsapp = request.data.get("whatsapp")
        otp_code = request.data.get("otp_code")

        if not whatsapp or not otp_code:
            return CustomResponse.bad_request("Silahkan masukkan nomor whatsapp dan kode OTP")

        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return CustomResponse.bad_request("Nomor Whatsapp yang Anda masukkan tidak salah")

        if user.is_registered:
            return CustomResponse.bad_request("Whatsapp sudah terdaftar")

        if not user.otp.validate_otp(otp_code):
            return CustomResponse.bad_request("OTP tidak valid atau sudah kadaluarsa")

        user.is_registered = True
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        return CustomResponse.jwt(refresh)


class CustomUserModelViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny(),]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        whatsapp = request.data.get("whatsapp")
        user = self.queryset.filter(
            whatsapp=whatsapp, is_registered=False).first()
        if user is not None:
            # Jika user registrasi dengan nomor whatsapp yang sama
            # tapi belum menyelesaikan proses registrasi.
            # Maka akan dikirimkan ulang kode OTP
            user.full_name = request.data.get("full_name")
            user.otp.send_otp_wa()
            user.save()
            return CustomResponse.ok("OTP telah dikirim ke nomor whatsapp Anda")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.ok("Berhasil menambahkan data")
        return CustomResponse.serializers_erros(serializer.errors)


class ParentViewSet(CustomUserModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ParentRegistrationSerializer
        return super().get_serializer_class()


class MidwifeViewSet(CustomUserModelViewSet):
    queryset = Midwife.objects.all()
    serializer_class = MidwifeSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return MidwifeRegistrationSerializer
        return super().get_serializer_class()


class CadreViewSet(CustomUserModelViewSet):
    queryset = Cadre.objects.all()
    serializer_class = CadreSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CadreRegistrationSerializer
        return super().get_serializer_class()


class PuskesmasViewSet(CustomUserModelViewSet):
    queryset = Puskesmas.objects.all()
    serializer_class = PuskesmasSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PuskesmasRegistrationSerializer
        return super().get_serializer_class()
