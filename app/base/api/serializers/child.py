from rest_framework import serializers

from base.models import Child


class ChildSerializer(serializers.ModelSerializer):
    is_measured = serializers.SerializerMethodField()
    class Meta:
        model = Child
        fields = '__all__'

    def get_is_measured(self, obj):
        if not self.context['child_measured']:
            return None
        child_measured = self.context['child_measured']
        if obj in child_measured:
            return True