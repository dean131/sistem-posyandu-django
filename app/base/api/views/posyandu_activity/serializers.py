"""
PosyanduActivity Serializer
"""
from rest_framework import serializers

from base.models import PosyanduActivity


class PosyanduActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PosyanduActivity
        fields = '__all__'