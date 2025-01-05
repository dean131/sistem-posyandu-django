from rest_framework import serializers

from village.models import Village


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = "__all__"
