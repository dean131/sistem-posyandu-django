from rest_framework import serializers

from posyandu.models import Posyandu
from child.models import Child


class PosyanduSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posyandu
        fields = "__all__"
        depth = 1


class ChildSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    current_age = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = "__all__"

    def get_parent_name(self, obj):
        return obj.parent.full_name

    def get_current_age(self, obj):
        return obj.current_age
