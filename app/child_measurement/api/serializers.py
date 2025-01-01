from rest_framework import serializers

from child_measurement.models import ChildMeasurement


class ChildMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildMeasurement
        fields = "__all__"
