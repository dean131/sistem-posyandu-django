

from rest_framework import serializers

from account.models import (
    User, 
    Parent, 
    Midwife, 
    Cadre, 
    Puskesmas,
    OTP,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class MidwifeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Midwife
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadre
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CadreProfileSerializer(CadreSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return obj.profile


class PuskesmasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puskesmas
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    def send_otp_wa(self, user):
        otp, created = OTP.objects.get_or_create(user=user)
        otp.send_otp_wa()


    def create(self, validated_data):
        instance = self.Meta.model.objects.create_user(**validated_data)
        self.send_otp_wa(instance)
        return instance


class ParentRegistrationSerializer(ParentSerializer, RegisterSerializer):
    pass


class MidwifeRegistrationSerializer(MidwifeSerializer, RegisterSerializer):
    pass
    
    
class CadreRegistrationSerializer(CadreSerializer, RegisterSerializer):
    pass


class PuskesmasRegistrationSerializer(PuskesmasSerializer, RegisterSerializer):
    pass