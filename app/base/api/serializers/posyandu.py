from rest_framework import serializers

from base.models import Posyandu


class PosyanduSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posyandu
        fields = '__all__'