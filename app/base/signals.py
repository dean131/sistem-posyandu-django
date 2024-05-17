from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import (
    Child,
    GrowthChart,
    ChildMeasurement
)


# Membuat GrowthChart setiap kali Child baru dibuat
@receiver(post_save, sender=Child)
def create_child_growchart(sender, instance, created, **kwargs):
    if created:
        GrowthChart.objects.create(child=instance)
        ChildMeasurement.objects.create(
            child=instance,
            height=instance.birth_height,
            weight=instance.birth_weight,
        )



