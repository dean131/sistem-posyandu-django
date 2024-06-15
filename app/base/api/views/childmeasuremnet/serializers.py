from rest_framework import serializers

from base.models import ChildMeasurement


class ChildMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildMeasurement
        fields = '__all__'
