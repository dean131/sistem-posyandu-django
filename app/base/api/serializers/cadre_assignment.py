from rest_framework import serializers

from base.models import CadreAssignment


class CadreAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadreAssignment
        fields = '__all__'