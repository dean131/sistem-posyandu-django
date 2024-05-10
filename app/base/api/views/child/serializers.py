"""
Child Serializrs
"""
from rest_framework import serializers

from base.models import Child, GrowthChart


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class ChildInfoSerializer(serializers.ModelSerializer):
    growthchart = serializers.SerializerMethodField()
    current_age = serializers.SerializerMethodField()
    current_age_month = serializers.SerializerMethodField()
    class Meta:
        model = Child
        fields = '__all__'
        depth = 1

    def get_growthchart(self, obj):
        return GrowthChartSerializer(obj.growthchart, context=self.context).data
    
    def get_current_age(self, obj):
        return obj.current_age
    
    def get_current_age_month(self, obj):
        return obj.curent_age_in_months
    

class GrowthChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthChart
        fields = '__all__'