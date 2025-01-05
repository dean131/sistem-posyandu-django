from rest_framework import serializers

from account.models import (
    CadreProfile,
    MidwifeProfile,
    ParentProfile,
    Parent,
    Midwife,
    Cadre,
    Puskesmas,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class ParentSerializer(UserSerializer):
    class Meta:
        model = Parent
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class MidwifeSerializer(UserSerializer):

    class Meta:
        model = Midwife
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class CadreSerializer(UserSerializer):
    class Meta:
        model = Cadre
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class PuskesmasSerializer(UserSerializer):
    class Meta:
        model = Puskesmas
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class ParentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentProfile
        fields = "__all__"


class MidwifeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidwifeProfile
        fields = "__all__"


class CadreProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadreProfile
        fields = "__all__"
