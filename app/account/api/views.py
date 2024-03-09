from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
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
        if self.action == "login_password":
            return [AllowAny(),]
        return super().get_permissions()

    @action(detail=False, methods=["post"])
    def login_password(self, request):
        whatsapp = request.data.get("whatsapp")
        password = request.data.get("password")

        user = authenticate(request, whatsapp=whatsapp, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"message": _("Invalid whatsapp or password.")})
    

class ParentViewSet(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ParentRegistrationSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny(),]
        return super().get_permissions()


class MidwifeViewSet(ModelViewSet):
    queryset = Midwife.objects.all()
    serializer_class = MidwifeSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return MidwifeRegistrationSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny(),]
        return super().get_permissions()
    

class CadreViewSet(ModelViewSet):
    queryset = Cadre.objects.all()
    serializer_class = CadreSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny(),]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == "create":
            return CadreRegistrationSerializer
        return super().get_serializer_class()