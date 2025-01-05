from django.db import models

# Create your models here.
from posyandu.models import Posyandu


class PosyanduActivity(models.Model):
    """
    Merepresentasikan sebuah Kegiatan yang dilakukan di Posyandu.
    """

    name = models.CharField(max_length=255, default="Kegiatan Posyandu")
    description = models.TextField(blank=True, null=True)
    date = models.DateField(null=True)
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    posyandu = models.ForeignKey(Posyandu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} di {self.posyandu.name}"
