from datetime import date

from django.db import models
from django.conf import settings


class Village(models.Model):
    """
    Merepresentasikan sebuah Desa.
    Hanya dapat di-CRUD oleh pihak Puskesmas.
    """

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    puskesmas = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)


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
    village = models.ForeignKey(Village, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.midwife.full_name} di {self.village.name}"
    

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
    description = models.TextField(blank=True, null=True)
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

    national_id_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    birth_order = models.PositiveIntegerField()
    birth_weight = models.FloatField()
    birth_height = models.FloatField()
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
    
    @property
    def current_age(self):
        """
        Menghitung usia anak saat ini.
        """

        today = date.today()
        birth_date = self.birth_date

        years = today.year - birth_date.year
        months = today.month - birth_date.month

        if months < 0:
            years -= 1
            months += 12

        return f"{years} tahun, {months} bulan"


class ChildMeasurement(models.Model):
    """
    Merepresentasikan pengukuran seorang Anak.
    """

    MEASUREMENT_METHOD_CHOICES = [
        ("STANDING", "Standing"),
        ("SUPINE", "Supine"),
    ]

    WEIGHT_GAIN_CHOICES = [
        ("O", "O"),
        ("T", "T")
    ]

    weight = models.FloatField()
    height = models.FloatField()
    # lingkar kepala
    head_circumference = models.FloatField()
    # usia saat pengukuran dalam tahun, bulan, hari
    age = models.CharField(max_length=50, null=True, blank=True)
    # cara ukur
    measurement_method = models.CharField(max_length=8, choices=MEASUREMENT_METHOD_CHOICES)
    # lingkar lengan atas / lila
    arm_circumference = models.FloatField()
    # bb/u
    weight_for_age = models.CharField(max_length=255)
    # z score bb/u
    z_score_weight_for_age = models.FloatField()
    # tb/u
    height_for_age = models.CharField(max_length=255)
    # z score tb/u
    z_score_height_for_age = models.FloatField()
    # bb/tb
    weight_for_height = models.CharField(max_length=255)
    # z score bb/tb 
    z_score_weight_for_height = models.FloatField()
    # naik berat badan
    weight_gain = models.CharField(max_length=1, choices=WEIGHT_GAIN_CHOICES)
    # pmt diterima (kg)
    pmt_received = models.FloatField(blank=True, null=True)
    # jumlah vitamin A
    vitamin_a_count = models.PositiveIntegerField(blank=True, null=True)
    # kpsp
    kpsp = models.BooleanField(blank=True, null=True)
    # kia
    kia = models.BooleanField(blank=True, null=True)
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    posyandu_activity = models.ForeignKey(PosyanduActivity, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pengukuran Anak {self.child.full_name}"
    
    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super().save(*args, **kwargs)
    
    def calculate_age(self):
        """
        Menghitung usia dari tanggal lahir.

        Args:
            birthdate: Tanggal lahir dalam format YYYY-MM-DD.

        Returns:
            Usia dalam format "tahun, bulan, hari".
        """

        today = date.today()
        birth_date = date.fromisoformat(self.child.birth_date)

        years = today.year - birth_date.year
        months = today.month - birth_date.month

        if months < 0:
            years -= 1
            months += 12

        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            days += birth_date.day

        return f"{years} tahun, {months} bulan, {days} hari"


class ParentPosyandu(models.Model):
    """
    Merepresentasikan seorang Orang Tua yang terdaftar di Posyandu.
    """
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posyandu = models.ForeignKey(Posyandu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.parent.full_name} di {self.posyandu.name}"


class LengthForAgeBoys(models.Model):
    """
    Merepresentasikan data standard panjang badan untuk anak laki-laki 
    untuk umur 0-24 bulan.
    """
    age_months = models.PositiveSmallIntegerField(verbose_name="Umur (bulan)", unique=True)
    sd_minus_3 = models.FloatField(verbose_name="-3 SD")
    sd_minus_2 = models.FloatField(verbose_name="-2 SD")
    sd_minus_1 = models.FloatField(verbose_name="-1 SD")
    median = models.FloatField(verbose_name="Median")
    sd_plus_1 = models.FloatField(verbose_name="+1 SD")
    sd_plus_2 = models.FloatField(verbose_name="+2 SD")
    sd_plus_3 = models.FloatField(verbose_name="+3 SD")

    def __str__(self):
        return f"Umur: {self.age_months} bulan"
    

class LengthForAgeGirls(models.Model):
    """
    Merepresentasikan data standard panjang badan untuk anak perempuan 
    untuk umur 0-24 bulan.
    """
    age_months = models.PositiveSmallIntegerField(verbose_name="Umur (bulan)", unique=True)
    sd_minus_3 = models.FloatField(verbose_name="-3 SD")
    sd_minus_2 = models.FloatField(verbose_name="-2 SD")
    sd_minus_1 = models.FloatField(verbose_name="-1 SD")
    median = models.FloatField(verbose_name="Median")
    sd_plus_1 = models.FloatField(verbose_name="+1 SD")
    sd_plus_2 = models.FloatField(verbose_name="+2 SD")
    sd_plus_3 = models.FloatField(verbose_name="+3 SD")

    def __str__(self):
        return f"Umur: {self.age_months} bulan"
    

class HeightForAgeBoys(models.Model):
    """
    Merepresentasikan data standard tinggi badan untuk anak laki-laki 
    untuk umur 0-24 bulan.
    """
    age_months = models.PositiveSmallIntegerField(verbose_name="Umur (bulan)", unique=True)
    sd_minus_3 = models.FloatField(verbose_name="-3 SD")
    sd_minus_2 = models.FloatField(verbose_name="-2 SD")
    sd_minus_1 = models.FloatField(verbose_name="-1 SD")
    median = models.FloatField(verbose_name="Median")
    sd_plus_1 = models.FloatField(verbose_name="+1 SD")
    sd_plus_2 = models.FloatField(verbose_name="+2 SD")
    sd_plus_3 = models.FloatField(verbose_name="+3 SD")

    def __str__(self):
        return f"Umur: {self.age_months} bulan"
    

class HeightForAgeGirls(models.Model):
    """
    Merepresentasikan data standard tinggi badan untuk anak perempuan 
    untuk umur 0-24 bulan.
    """
    age_months = models.PositiveSmallIntegerField(verbose_name="Umur (bulan)", unique=True)
    sd_minus_3 = models.FloatField(verbose_name="-3 SD")
    sd_minus_2 = models.FloatField(verbose_name="-2 SD")
    sd_minus_1 = models.FloatField(verbose_name="-1 SD")
    median = models.FloatField(verbose_name="Median")
    sd_plus_1 = models.FloatField(verbose_name="+1 SD")
    sd_plus_2 = models.FloatField(verbose_name="+2 SD")
    sd_plus_3 = models.FloatField(verbose_name="+3 SD")

    def __str__(self):
        return f"Umur: {self.age_months} bulan"