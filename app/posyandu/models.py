from django.db import models

from village.models import Village
from account.models import Parent


# Create your models here.
class Posyandu(models.Model):
    """
    Meresentasikan sebuah Posyandu.
    Hanya dapat di-CRUD oleh pihak Puskesmas.
    """

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    parents = models.ManyToManyField(Parent, related_name="posyandus")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
