from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from child_measurement.models import GrowthChart
from child.models import Child


from .models import (
    Parent,
    Midwife,
    Cadre,
    Puskesmas,
    Address,
    ParentProfile,
    MidwifeProfile,
    CadreProfile,
    PuskesmasProfile,
)


# Membuat Profile setiap kali akun Parent baru dibuat
@receiver(post_save, sender=Parent)
def create_parent_profile(sender, instance, created, **kwargs):
    if created:
        ParentProfile.objects.create(user=instance)
        Address.objects.create(user=instance)


# Membuat Profile setiap kali akun Cadre baru dibuat
@receiver(post_save, sender=Cadre)
def create_cadre_profile(sender, instance, created, **kwargs):
    if created:
        CadreProfile.objects.create(user=instance)
        Address.objects.create(user=instance)


# Membuat Profile setiap kali akun Midwife baru dibuat
@receiver(post_save, sender=Midwife)
def create_midwife_profile(sender, instance, created, **kwargs):
    if created:
        MidwifeProfile.objects.create(user=instance)
        Address.objects.create(user=instance)


# Membuat Profile setiap kali akun Puskesmas baru dibuat
@receiver(post_save, sender=Puskesmas)
def create_puskesmas_profile(sender, instance, created, **kwargs):
    if created:
        PuskesmasProfile.objects.create(user=instance)
        Address.objects.create(user=instance)
