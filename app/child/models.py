from django.db import models
from datetime import date
from account.models import Parent

# Create your models here.


class Child(models.Model):
    """
    Merepresentasikan seorang Anak.
    """

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    national_id_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    birth_order = models.PositiveIntegerField()
    birth_weight = models.FloatField()
    birth_height = models.FloatField()
    # kia_number = models.CharField(max_length=50, null=True, blank=True)
    # imd_number = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to="child_pictures/", null=True, blank=True)
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    @property
    def current_age(self):
        """
        Menghitung usia anak saat ini.
        """
        birth = self.birth_date
        today = date.today()
        days = (today - birth).days
        months = 0
        years = 0
        while days >= 365.25:
            days -= 365.25
            years += 1
        while days >= 30.55:
            days -= 30.55
            months += 1
        return f"{years} tahun, {months} bulan"

    @property
    def curent_age_in_months(self):
        """
        Menghitung usia anak dalam bulan.

        Returns:
            Usia anak dalam bulan.
        """

        today = date.today()
        birth_date = self.birth_date

        years = today.year - birth_date.year
        months = today.month - birth_date.month

        if months < 0:
            years -= 1
            months += 12

        return years * 12 + months

    @property
    def growthchart(self):
        return self.growthchart_set.all()
