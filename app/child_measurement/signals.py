from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# from child_measurement.models import Child, GrowthChart


# @receiver(post_save, sender=Child)
# def create_growth_chart(sender, instance, created, **kwargs):
#     """
#     Signal to create an empty GrowthChart when a new Child is created.
#     """
#     if created:
#         GrowthChart.objects.get_or_create(child=instance)


# # Membuat GrowthChart setiap kali Child baru dibuat
# @receiver(post_save, sender=Child)
# def create_child_growchart(sender, instance, created, **kwargs):
#     if created:
#         GrowthChart.objects.create(child=instance)
#         instance.birth_date = datetime.now().date()
#         ChildMeasurement.objects.create(
#             child=instance,
#             height=instance.birth_height,
#             weight=instance.birth_weight,
#         )
