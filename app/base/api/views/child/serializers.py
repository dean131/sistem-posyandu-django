"""
Child Serializrs
"""
from rest_framework import serializers

from base.models import Child, GrowthChart


class ChildSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    current_age = serializers.SerializerMethodField()
    current_age_month = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = '__all__'

    def get_parent_name(self, obj):
        return obj.parent.full_name
    
    def get_current_age(self, obj):
        return obj.current_age
    
    def get_current_age_month(self, obj):
        return obj.curent_age_in_months
    
    def get_parent_name(self, obj):
        return obj.parent.full_name


class ChildInfoSerializer(ChildSerializer):
    growthchart = serializers.SerializerMethodField()

    def get_growthchart(self, obj):
        return GrowthChartSerializer(obj.growthchart, context=self.context).data
    

class GrowthChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthChart
        fields = '__all__'