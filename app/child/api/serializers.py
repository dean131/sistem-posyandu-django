from matplotlib.pyplot import cla
from rest_framework import serializers

from child.models import Child
from child_measurement.models import ChildMeasurement, GrowthChart


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = "__all__"


class CreateChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = "__all__"


class UpdateChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        exclude = ("parent",)


# EXTERNAL
class GrowthChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthChart
        fields = "__all__"


class ChildMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildMeasurement
        fields = "__all__"
