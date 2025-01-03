from rest_framework import serializers

from child_measurement.models import ChildMeasurement, GrowthChart


class ListChildMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildMeasurement
        fields = "__all__"
        depth = 1


class CreateChildMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildMeasurement
        fields = "__all__"
