from django.db import models
from django.conf import settings


class Village(models.Model):
    """
    Merepresentasikan sebuah Desa.
    Hanya dapat di-CRUD oleh pihak Puskesmas.
    """

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    puskesmas = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Posyandu(models.Model):
    """
    Meresentasikan sebuah Posyandu.
    Hanya dapat di-CRUD oleh pihak Puskesmas.
    """

    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    village = models.ForeignKey(Village, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class MidwifeAssignment(models.Model):
    """
    Merepresentasikan penugasan seorang Bidan di sebuah Desa.
    """
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    midwife = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Village = models.ForeignKey(Village, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.midwife.full_name} di {self.Village.name}"
    

class CadreAssignment(models.Model):
    """
    Merepresentasikan penugasan seorang Kader di sebuah Posyandu.
    """
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    cadre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posyandu = models.ForeignKey(Posyandu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cadre.full_name} di {self.posyandu.name}"
    

class PosyanduActivity(models.Model):
    """
    Merepresentasikan sebuah Kegiatan yang dilakukan di Posyandu.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    posyandu = models.ForeignKey(Posyandu, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Child(models.Model):
    """
    Merepresentasikan seorang Anak.
    """

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    national_id_number = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    birth_order = models.PositiveIntegerField()
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2)
    birth_height = models.DecimalField(max_digits=5, decimal_places=2)
    kia_number = models.CharField(max_length=50, null=True, blank=True)
    imd_number = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to="child_pictures/", null=True, blank=True)
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.full_name
    

class ChildMeasurement(models.Model):
    """
    Merepresentasikan pengukuran seorang Anak.
    """

    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    # lingkar kepala
    head_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    # usia saat pengukuran dalam bulan
    age = models.PositiveIntegerField()
    # cara ukur
    measurement_method = models.CharField(max_length=255)
    # lingkar lengan atas / lila
    arm_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    # bb/u
    weight_for_age = models.CharField(max_length=255)
    # z score bb/u
    z_score_weight_for_age = models.DecimalField(max_digits=5, decimal_places=2)
    # tb/u
    height_for_age = models.CharField(max_length=255)
    # z score tb/u
    z_score_height_for_age = models.DecimalField(max_digits=5, decimal_places=2)
    # bb/tb
    weight_for_height = models.CharField(max_length=255)
    # z score bb/tb 
    z_score_weight_for_height = models.DecimalField(max_digits=5, decimal_places=2)
    # naik berat badan
    weight_gain = models.CharField(max_length=255)
    # pmt diterima (kg)
    pmt_received = models.DecimalField(max_digits=5, decimal_places=2)
    # jumlah vitamin A
    vitamin_a_count = models.PositiveIntegerField()
    # kpsp
    kpsp = models.BooleanField()
    # kia
    kia = models.BooleanField()
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    posyandu_activity = models.ForeignKey(PosyanduActivity, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pengukuran Anak {self.child.full_name}"
