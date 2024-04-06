from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import (
    User, 
    Parent, 
    Midwife, 
    Cadre,
    Puskesmas,

    ParentProfile,
    MidwifeProfile,
    CadreProfile,
    PuskesmasProfile,
)


@receiver(post_save, sender=Parent)
def create_parent_profile(sender, instance, created, **kwargs):
    if created:
        ParentProfile.objects.create(user=instance)


@receiver(post_save, sender=Cadre)
def create_cadre_profile(sender, instance, created, **kwargs):
    if created:
        CadreProfile.objects.create(user=instance)


@receiver(post_save, sender=Midwife)
def create_midwife_profile(sender, instance, created, **kwargs):
    if created:
        MidwifeProfile.objects.create(user=instance)


@receiver(post_save, sender=Puskesmas)
def create_puskesmas_profile(sender, instance, created, **kwargs):
    if created:
        PuskesmasProfile.objects.create(user=instance)

