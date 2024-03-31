from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from account.api.serializers import (
    UserSerializer, 

    ParentSerializer,
    ParentRegistrationSerializer,

    MidwifeSerializer,
    MidwifeRegistrationSerializer,

    CadreSerializer,
    CadreRegistrationSerializer,
)

from account.models import (
    User, 
    Parent, 
    Midwife, 
    Cadre
)

from posyanduapp.utils.custom_response import CustomResponse


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]

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
            return Response(
                {"message": _("Silahkan masukkan nomor whatsapp dan password")},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, whatsapp=whatsapp, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            refresh["role"] = user.role
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": _("Kredential tidak valid")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @action(detail=False, methods=["post"])
    def login_otp(self, request):
        whatsapp = request.data.get("whatsapp")

        if not whatsapp:
            return Response(
                {"message": _("Silahkan masukkan nomor whatsapp Anda")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return Response(
                {"message": _("Pengguna tidak ditemukan")},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not user.is_registered:
            return Response(
                {"message": _("Nomor whatsapp belum terdaftar")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.otp.send_otp_wa()
        return Response(
            {"message": _("OTP telah dikirim ke nomor whatsapp Anda")},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=["post"])
    def login_otp_validate(self, request):
        whatsapp = request.data.get("whatsapp")
        otp_code = request.data.get("otp_code")

        if not whatsapp or not otp_code:
            return Response(
                {"message": _("Silahkan masukkan nomor whatsapp dan kode OTP")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return Response(
                {"message": _("Akun tidak ditemukan")},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not user.is_registered:
            return Response(
                {"message": _("Akun belum terdaftar")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.otp.validate_otp(otp_code):
            return Response(
                {"message": _("OTP tidak valid atau sudah kadaluarsa")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=["post"])
    def register_otp_validate(self, request):
        whatsapp = request.data.get("whatsapp")
        otp_code = request.data.get("otp_code")

        if not whatsapp or not otp_code:
            return Response(
                {"message": _("Silahkan masukkan nomor whatsapp dan kode OTP")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.filter(whatsapp=whatsapp).first()
        if user is None:
            return Response(
                {"message": _("Nomor Whatsapp yang Anda masukkan tidak salah")},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user.is_registered:
            return Response(
                {"message": _("Whatsapp sudah terdaftar")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.otp.validate_otp(otp_code):
            return Response(
                {"message": _("OTP tidak valid atau sudah kadaluarsa")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.is_registered = True
        user.save()
        
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK
        )


class CustomUserModelViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny(),]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        whatsapp = request.data.get("whatsapp")
        user = self.queryset.filter(whatsapp=whatsapp, is_registered=False).first()
        if user is not None:
            # update user fullname
            user.fullname = request.data.get("full_name")
            user.otp.send_otp_wa()
            user.save()
            return Response(
                {"message": _("OTP telah dikirim ke nomor whatsapp Anda")},
                status=status.HTTP_200_OK
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return CustomResponse.ok("Data berhasil dibuat")
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