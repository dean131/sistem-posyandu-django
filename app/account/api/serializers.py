

from rest_framework import serializers

from account.models import (
    CadreProfile,
    MidwifeProfile,
    ParentProfile,
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
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Parent
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_profile(self, obj):
        return ParentProfileSerializer(obj.profile).data


class ParentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentProfile
        fields = '__all__'


class MidwifeSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Midwife
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_profile(self, obj):
        return MidwifeProfileSerializer(obj.profile).data


class MidwifeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidwifeProfile
        fields = '__all__'


class CadreSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Cadre
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_profile(self, obj):
        return CadreProfileSerializer(obj.profile).data


class CadreProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadreProfile
        fields = '__all__'


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
