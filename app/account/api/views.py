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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]

    def get_permissions(self):
        if self.action in ["login_password", "login_otp", "login_otp_validate"]:
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
        
        user = User.objects.filter(whatsapp=whatsapp, is_active=True).first()
        if user is None:
            return Response(
                {"message": _("Pengguna tidak ditemukan")},
                status=status.HTTP_404_NOT_FOUND
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
        
        user = User.objects.filter(whatsapp=whatsapp, is_active=True).first()
        if user is None:
            return Response(
                {"message": _("Pengguna tidak ditemukan")},
                status=status.HTTP_404_NOT_FOUND
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
        
        user = User.objects.filter(whatsapp=whatsapp, is_active=False).first()
        if user is None:
            return Response(
                {"message": _("Pengguna tidak ditemukan")},
                status=status.HTTP_404_NOT_FOUND
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


class CustomUserModelViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny(),]
        return super().get_permissions()


class ParentViewSet(CustomUserModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ParentRegistrationSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        user = Parent.objects.filter(whatsapp=request.data.get("whatsapp")).first()
        if user is not None and not user.profile.is_complete:
            user.otp.send_otp_wa()
            user.save()
            return Response(
                {"message": _("OTP telah dikirim ke nomor whatsapp Anda")},
                status=status.HTTP_200_OK
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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