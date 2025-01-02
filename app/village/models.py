from django.db import models

from django.conf import settings

from account.models import Midwife, Puskesmas


class Village(models.Model):
    """
    Merepresentasikan sebuah Desa.
    Hanya dapat di-CRUD oleh pihak Puskesmas.
    """

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
    midwifes = models.ManyToManyField(Midwife, related_name="villages")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)
