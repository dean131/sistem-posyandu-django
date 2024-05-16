from rest_framework import serializers

from base.models import Child, Posyandu


class PosyanduSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posyandu
        fields = '__all__'
        depth = 1


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
