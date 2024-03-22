from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User, ParentProfile, Parent, Midwife, Cadre


@receiver(post_save, sender=Parent)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ParentProfile.objects.create(user=instance)
