"""
PosyanduActivity Serializer
"""
from rest_framework import serializers

from base.models import Child, PosyanduActivity


class PosyanduActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PosyanduActivity
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):
    is_measured = serializers.SerializerMethodField()
    
    class Meta:
        model = Child
        fields = '__all__'

    def get_is_measured(self, obj):
        if not self.context['child_measured_ids']:
            return None
        child_measured_ids = self.context['child_measured_ids']
        for child_id in child_measured_ids:
            if obj.id == child_id:
                return True
        return False