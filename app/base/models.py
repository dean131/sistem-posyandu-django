import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from datetime import date
import numpy as np
import io

from django.db import models
from django.conf import settings
from django.core.files.images import ImageFile

from account.models import Cadre, Midwife, Parent


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
    midwife = models.ForeignKey(Midwife, on_delete=models.CASCADE)
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
    cadre = models.ForeignKey(Cadre, on_delete=models.CASCADE)
    posyandu = models.ForeignKey(Posyandu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cadre.full_name} di {self.posyandu.name}"
    

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
        return f"{years} tahun, {months} bulan, {int(days)} hari"
    
    @property
    def parent_name(self):
        return self.parent.full_name
    
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
    
    # @property
    # def is_measured(self):


class ParentPosyandu(models.Model):
    """
    Merepresentasikan seorang Orang Tua yang terdaftar di Posyandu.
    """
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
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
        return f"PB/U-L: {self.age_months} bulan"
    
    @property
    def title(self):
        return "Panjang Badan/Umur Laki-laki (0-24 bulan)"
    
    @property
    def xlabel(self):
        return "Umur (bulan)"
    
    @property
    def ylabel(self):
        return "Panjang Badan (cm)"
    

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
        return f"PB/U-P: {self.age_months} bulan"
    
    @property
    def title(self):
        return "Panjang Badan/Umur Perempuan (0-24 bulan)"
    
    @property
    def xlabel(self):
        return "Umur (bulan)"
    
    @property
    def ylabel(self):
        return "Panjang Badan (cm)"
    

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
        return f"TB/U-L: {self.age_months} bulan"
    
    @property
    def title(self):
        return "Tinggi Badan/Umur Laki-laki (24-60 bulan)"
    
    @property
    def xlabel(self):
        return "Umur (bulan)"
    
    @property
    def ylabel(self):
        return "Tinggi Badan (cm)"
    

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
        return f"TB/U-P: {self.age_months} bulan"
    
    @property
    def title(self):
        return "Tinggi Badan/Umur Perempuan (24-60 bulan)"
    
    @property
    def xlabel(self):
        return "Umur (bulan)"
    
    @property
    def ylabel(self):
        return "Tinggi Badan (cm)"
    

class WeightForAgeBoys(models.Model):
    """
    Merepresentasikan data standard berat badan untuk anak laki-laki umur 0-60 bulan.
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
        return f"BB/U-L: {self.age_months} bulan"
    
    @property
    def title(self):
        return "Berat Badan/Umur Laki-laki (0-60 bulan)"
    
    @property
    def xlabel(self):
        return "Umur (bulan)"
    
    @property
    def ylabel(self):
        return "Berat Badan (Kg)"
    

class WeightForAgeGirls(models.Model):
    """
    Merepresentasikan data standard berat badan untuk anak perempuan umur 0-60 bulan.
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
        return f"BB/U-P: {self.age_months} bulan"
    
    @property
    def title(self):
        return "Berat Badan/Umur Perempuan (0-60 bulan)"
    
    @property
    def xlabel(self):
        return "Umur (bulan)"
    
    @property
    def ylabel(self):
        return "Berat Badan (Kg)"


class GrowthChart(models.Model):
    """
    Merepresentasikan data grafik pertumbuhan anak.
    """
    legth_for_age_chart = models.ImageField(upload_to="growth_charts/", null=True, blank=True)
    height_for_age_chart = models.ImageField(upload_to="growth_charts/", null=True, blank=True)
    weight_for_age_chart_0_24 = models.ImageField(upload_to="growth_charts/", null=True, blank=True)
    weight_for_age_chart_24_60 = models.ImageField(upload_to="growth_charts/", null=True, blank=True)
    weight_for_height_chart = models.ImageField(upload_to="growth_charts/", null=True, blank=True)
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    child = models.OneToOneField(Child, on_delete=models.CASCADE)

    def __str__(self):
        return f"Grafik Pertumbuhan {self.child.full_name}"


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
    head_circumference = models.FloatField(null=True, blank=True)
    # usia saat pengukuran dalam tahun, bulan, hari
    age = models.CharField(max_length=50, null=True, blank=True)
    # usia dalam bulan
    age_in_month = models.PositiveIntegerField(null=True, blank=True)
    # cara ukur
    measurement_method = models.CharField(max_length=8, choices=MEASUREMENT_METHOD_CHOICES, null=True, blank=True)
    # lingkar lengan atas / lila
    arm_circumference = models.FloatField(null=True, blank=True)
    # bb/u
    weight_for_age = models.CharField(max_length=255, null=True, blank=True)
    # z score bb/u
    z_score_weight_for_age = models.FloatField(null=True, blank=True)
    # tb/u
    height_for_age = models.CharField(max_length=255, null=True, blank=True)
    # z score tb/u
    z_score_height_for_age = models.FloatField(null=True, blank=True)
    # bb/tb
    weight_for_height = models.CharField(max_length=255, null=True, blank=True)
    # z score bb/tb 
    z_score_weight_for_height = models.FloatField(null=True, blank=True)
    # naik berat badan
    weight_gain = models.CharField(max_length=1, choices=WEIGHT_GAIN_CHOICES, null=True, blank=True)
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
        if not self.id:
            self.set_ages()
        self.calculate_length_and_height_for_age()
        self.calculate_weight_for_age()
        super().save(*args, **kwargs)

    def set_ages(self):
        self.age = self.child.current_age
        self.age_in_month = self.child.curent_age_in_months

    def calculate_length_and_height_for_age(self):
        def get_queryset_length_for_age(gender, child_age):
            if gender == "M":
                if child_age < 24:
                    queryset = LengthForAgeBoys.objects.all()
                else:
                    queryset = HeightForAgeBoys.objects.all()
            else:
                if child_age < 24:
                    queryset = LengthForAgeGirls.objects.all()
                else:
                    queryset = HeightForAgeGirls.objects.all()
            return queryset
        
        def determine_sd_difference_length_for_age(sd):
            height_median_difference = self.height - sd.median
            if height_median_difference < 0:
                sd_difference = sd.median - sd.sd_minus_1
            else:
                sd_difference = sd.sd_plus_1 - sd.median
            return sd_difference
        
        # get queryset
        child_age = self.age_in_month
        gender = self.child.gender
        queryset = get_queryset_length_for_age(gender, child_age)
        # get standard data
        sd = queryset.filter(age_months=child_age).first()
        height = self.height
        median = sd.median
        height_median_difference = height - median
        sd_difference = determine_sd_difference_length_for_age(sd=sd)
        # calculate z score
        z_score = height_median_difference / sd_difference
        # determine height for age z score
        self.z_score_height_for_age = z_score
        # determine height for age category
        if (z_score < -3):
            self.height_for_age = "Sangat Pendek"
        elif (z_score >= -3) and (z_score < -2):    
            self.height_for_age = "Pendek"
        elif (z_score >= -2) and (z_score < 3):
            self.height_for_age = "Normal"
        else:
            self.height_for_age = "Tinggi"  

        # Create the chart
        age = np.array([])
        min_1 = np.array([])
        min_2 = np.array([])
        min_3 = np.array([])
        median = np.array([])
        pos_1 = np.array([])
        pos_2 = np.array([])
        pos_3 = np.array([])

        for row in queryset:
            age = np.append(age, row.age_months)
            min_3 = np.append(min_3, row.sd_minus_3)
            min_2 = np.append(min_2, row.sd_minus_2)
            min_1 = np.append(min_1, row.sd_minus_1)
            median = np.append(median, row.median)
            pos_1 = np.append(pos_1, row.sd_plus_1)
            pos_2 = np.append(pos_2, row.sd_plus_2)
            pos_3 = np.append(pos_3, row.sd_plus_3)

        # mengatur ukuran grafik
        plt.figure(figsize=(10, 5))

        plt.plot(age.astype(int), min_3.astype(float), label='-3 SD')
        plt.plot(age.astype(int), min_2.astype(float), label='-2 SD')
        # plt.plot(age.astype(int), min_1.astype(float), label='-1 SD')
        plt.plot(age.astype(int), median.astype(float), label='Median')
        # plt.plot(age.astype(int), pos_1.astype(float), label='+1 SD')
        plt.plot(age.astype(int), pos_2.astype(float), label='+2 SD')
        plt.plot(age.astype(int), pos_3.astype(float), label='+3 SD')
        
        # Menambah keterangan ke Grafik
        plt.title(sd.title)
        plt.ylabel(sd.ylabel)
        plt.xlabel(sd.xlabel)   
        plt.grid()
        plt.legend()

        # # step ticks for x axis
        # min_age = int(age.min())
        # max_age = int(age.max()+1)
        # plt.xticks(range(min_age, max_age))

        # # step ticks for y axis
        # min_height = int(min_3.min())
        # max_height = int(pos_3.max()+1)
        # plt.yticks(range(min_height, max_height, 5))

        # jika anak berumur < 24 bulan maka simpan grafik panjang badan
        # jika anak berumur >= 24 bulan maka simpan grafik tinggi badan
        if self.age_in_month < 24:
            # get child measurements history 
            measurements = ChildMeasurement.objects.filter(
                child=self.child,
                age_in_month__lte=24
            ).order_by('created_at')
            measure_height_for_age_history = []
            measure_age_history = []

            for measurement in measurements:
                # untuk menghindari duplikat data pada grafik
                if measurement.id == self.id: # bernilai true jika measurement sudah disimpan di database
                    measure_height_for_age_history.append(self.height)
                    measure_age_history.append(self.age_in_month)
                    continue
                measure_height_for_age_history.append(measurement.height)
                measure_age_history.append(measurement.age_in_month)
            # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
            if not self.id:
                measure_height_for_age_history.append(self.height)
                measure_age_history.append(self.age_in_month)

            # Tambahkan titik koordinat pertumbuhan anak
            plt.scatter(measure_age_history, measure_height_for_age_history, color='red', label='Pertumbuhan Anak')
            # Hubungkan titik koordinat dengan garis
            plt.plot(measure_age_history, measure_height_for_age_history, color='red', linestyle='dashed')

            ## 5 step ticks
            # min_age = int(age.min())
            # max_age = int(age.max()+1)
            # plt.xticks(range(min_age, max_age, 5))

            # Save the figure
            figure = io.BytesIO()
            plt.savefig(figure, format='png')
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.legth_for_age_chart:
                self.child.growthchart.legth_for_age_chart.delete()
            # save new image
            self.child.growthchart.legth_for_age_chart.save(f"{self.child.id}_length_for_age_chart.png", content_file)
            plt.close()
            figure.close()
        else:
            # get child measurements history 
            measurements = ChildMeasurement.objects.filter(
                child=self.child,
                age_in_month__gte=24
            ).order_by('created_at')
            measure_height_for_age_history = []
            measure_age_history = []

            for measurement in measurements:
                # untuk menghindari duplikat data pada grafik
                if measurement.id == self.id: # bernilai true jika measurement sudah disimpan di database
                    measure_height_for_age_history.append(self.height)
                    measure_age_history.append(self.age_in_month)
                    continue
                measure_height_for_age_history.append(measurement.height)
                measure_age_history.append(measurement.age_in_month)
            # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
            if not self.id:
                measure_height_for_age_history.append(self.height)
                measure_age_history.append(self.age_in_month)

            # Tambahkan titik koordinat pertumbuhan anak
            plt.scatter(measure_age_history, measure_height_for_age_history, color='red', label='Pertumbuhan Anak')
            # Hubungkan titik koordinat dengan garis
            plt.plot(measure_age_history, measure_height_for_age_history, color='red', linestyle='dashed')

            ## 5 step ticks
            # min_age = int(age.min())
            # max_age = int(age.max()+1)
            # plt.xticks(range(min_age, max_age, 5))

            # Save the figure
            figure = io.BytesIO()
            plt.savefig(figure, format='png')
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.height_for_age_chart:
                self.child.growthchart.height_for_age_chart.delete()

            # save new image
            self.child.growthchart.height_for_age_chart.save(f"{self.child.id}_height_for_age_chart.png", content_file)
            plt.close() 
            figure.close()


    def calculate_weight_for_age(self):
        def get_queryset_weight_for_age(gender, child_age):
            if gender == "M":
                if child_age < 24:
                    queryset = WeightForAgeBoys.objects.filter(age_months__lt=24)
                else:
                    queryset = WeightForAgeBoys.objects.filter(age_months__gte=24)
            else:
                if child_age < 24:
                    queryset = WeightForAgeGirls.objects.filter(age_months__lt=24)
                else:
                    queryset = WeightForAgeGirls.objects.filter(age_months__gte=24)
            return queryset
        
        def determine_sd_difference_weight_for_age(sd):
            weight_median_difference = self.weight - sd.median
            if weight_median_difference < 0:
                sd_difference = sd.median - sd.sd_minus_1
            else:
                sd_difference = sd.sd_plus_1 - sd.median
            return sd_difference

        # get queryset
        gender = self.child.gender
        child_age = self.age_in_month
        queryset = get_queryset_weight_for_age(gender, child_age)
        # get standard data
        weight = self.weight
        child_age = self.age_in_month
        sd = queryset.filter(age_months=child_age).first()
        median = sd.median
        weight_median_difference = weight - median
        sd_difference = determine_sd_difference_weight_for_age(sd=sd)
        # calculate z score
        z_score = weight_median_difference / sd_difference
        # determine weight for age z score
        self.z_score_weight_for_age = z_score
        # determine weight for age category
        if (z_score < -3):
            self.weight_for_age = "Berat badan sangat kurang"
        elif (z_score >= -3) and (z_score < -2):    
            self.weight_for_age = "Berat badan kurang"
        elif (z_score >= -2) and (z_score <= 1):
            self.weight_for_age = "Berat badan normal"
        else:
            self.weight_for_age = "Resiko berat badan lebih"

        # Create the chart
        age = np.array([])
        min_3 = np.array([])
        min_2 = np.array([])
        min_1 = np.array([])
        median = np.array([])
        pos_1 = np.array([])
        pos_2 = np.array([])
        pos_3 = np.array([])

        for row in queryset:
            age = np.append(age, row.age_months)
            min_3 = np.append(min_3, row.sd_minus_3)
            min_2 = np.append(min_2, row.sd_minus_2)
            min_1 = np.append(min_1, row.sd_minus_1)
            median = np.append(median, row.median)
            pos_1 = np.append(pos_1, row.sd_plus_1)
            pos_2 = np.append(pos_2, row.sd_plus_2)
            pos_3 = np.append(pos_3, row.sd_plus_3)

        # mengatur ukuran grafik
        plt.figure(figsize=(10, 5))

        plt.plot(age.astype(int), min_3.astype(float), label='-3 SD')
        plt.plot(age.astype(int), min_2.astype(float), label='-2 SD')
        # plt.plot(age.astype(int), min_1.astype(float), label='-1 SD')
        plt.plot(age.astype(int), median.astype(float), label='Median')
        # plt.plot(age.astype(int), pos_1.astype(float), label='+1 SD')
        plt.plot(age.astype(int), pos_2.astype(float), label='+2 SD')
        plt.plot(age.astype(int), pos_3.astype(float), label='+3 SD')

        # Menambah keterangan ke Grafik
        plt.title(sd.title)
        plt.ylabel(sd.ylabel)
        plt.xlabel(sd.xlabel)   
        plt.grid()
        plt.legend()

        if self.age_in_month < 24:
            # get child measurements history
            measurements = ChildMeasurement.objects.filter(
                child=self.child,
                age_in_month__lte=24
            ).order_by('created_at')
        else:
            # get child measurements history
            measurements = ChildMeasurement.objects.filter(
                child=self.child,
                age_in_month__gte=24
            ).order_by('created_at')

        measure_weight_for_age_history = []
        measure_age_history = []

        for measurement in measurements:
            # untuk menghindari duplikat data pada grafik
            if measurement.id == self.id: # bernilai true jika measurement sudah disimpan di database
                measure_weight_for_age_history.append(self.weight)
                measure_age_history.append(self.age_in_month)
                continue
            measure_weight_for_age_history.append(measurement.weight)
            measure_age_history.append(measurement.age_in_month)
        # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
        if not self.id:
            measure_weight_for_age_history.append(self.weight)
            measure_age_history.append(self.age_in_month)
        
        # Tambahkan titik koordinat pertumbuhan anak
        plt.scatter(measure_age_history, measure_weight_for_age_history, color='red', label='Pertumbuhan Anak')
        # Hubungkan titik koordinat dengan garis
        plt.plot(measure_age_history, measure_weight_for_age_history, color='red', linestyle='dashed')

        # # step ticks for x axis
        # min_age = int(age.min())
        # max_age = int(age.max()+1)
        # plt.xticks(range(min_age, max_age))

        # # step ticks for y axis
        # min_weight = int(min_3.min())
        # max_weight = int(pos_3.max()+1)
        # plt.yticks(range(min_weight, max_weight))

        if self.age_in_month < 24:
            # Save the figure
            figure = io.BytesIO()
            plt.savefig(figure, format='png')
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.weight_for_age_chart_0_24:
                self.child.growthchart.weight_for_age_chart_0_24.delete()
            # save new image
            self.child.growthchart.weight_for_age_chart_0_24.save(f"{self.child.id}_weight_for_age_chart_0_24.png", content_file)
            plt.close()
            figure.close()
        else:
            # Save the figure
            figure = io.BytesIO()
            plt.savefig(figure, format='png')
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.weight_for_age_chart_24_60:
                self.child.growthchart.weight_for_age_chart_24_60.delete()
            # save new image
            self.child.growthchart.weight_for_age_chart_24_60.save(f"{self.child.id}_weight_for_age_chart_24_60.png", content_file)
            plt.close()
            figure.close()  

        
