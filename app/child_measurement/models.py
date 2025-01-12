from django.db import models
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from django.core.files.images import ImageFile
from child.models import Child
from posyandu_activity.models import PosyanduActivity

matplotlib.use("Agg")


class GrowthChart(models.Model):
    """
    Merepresentasikan data grafik pertumbuhan anak.
    """

    # WEIGHT FOR AGE 0-24
    weight_for_age_chart_0_24 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # WEIGHT FOR AGE 24-60
    weight_for_age_chart_24_60 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # LENGTH FOR AGE 0-24
    length_for_age_chart_0_24 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # HEIGHT FOR AGE 24-60
    height_for_age_chart_24_60 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # WEIGHT FOR LENGTH 0-24
    weight_for_length_chart_0_24 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # WEIGHT FOR HEIGTH 24-60
    weight_for_height_chart_24_60 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # BMI FOR AGE 0-24
    bmi_for_age_chart_0_24 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # BMI FOR AGE 24-60
    bmi_for_age_chart_24_60 = models.ImageField(
        upload_to="growth_charts/", null=True, blank=True
    )
    # Time Fields
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Foreign Keys
    child = models.OneToOneField(Child, on_delete=models.CASCADE)

    def __str__(self):
        return f"GrowthChart {self.child.full_name}"


class AnthropometricStandard(models.Model):
    """
    Merepresentasikan data standar antropometri.

    Attributes:
        index: merupakan umur atau tinggi badan dalam bulan atau cm.
    """

    GENDER_CHOICES = [
        ("M", "Laki-laki"),
        ("F", "Perempuan"),
    ]

    index = models.FloatField()
    sd_minus_3 = models.FloatField()
    sd_minus_2 = models.FloatField()
    sd_minus_1 = models.FloatField()
    median = models.FloatField()
    sd_plus_1 = models.FloatField()
    sd_plus_2 = models.FloatField()
    sd_plus_3 = models.FloatField()
    measurement_type = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.measurement_type}-{self.index}"


class ChildMeasurement(models.Model):
    """
    Merepresentasikan pengukuran seorang Anak.
    """

    MEASUREMENT_METHOD_CHOICES = [
        ("STANDING", "Standing"),
        ("SUPINE", "Supine"),
    ]

    WEIGHT_GAIN_CHOICES = [("O", "O"), ("T", "T")]

    weight = models.FloatField()
    height = models.FloatField()
    # lingkar kepala
    head_circumference = models.FloatField(null=True, blank=True)
    # usia saat pengukuran dalam tahun, bulan, hari
    age = models.CharField(max_length=50, null=True, blank=True)
    # usia dalam bulan
    age_in_month = models.PositiveIntegerField(null=True, blank=True)
    # cara ukur
    measurement_method = models.CharField(
        max_length=8, choices=MEASUREMENT_METHOD_CHOICES, null=True, blank=True
    )
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
    weight_gain = models.CharField(
        max_length=1, choices=WEIGHT_GAIN_CHOICES, null=True, blank=True
    )
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
    posyandu_activity = models.ForeignKey(
        PosyanduActivity, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Pengukuran Anak {self.child.full_name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self._set_ages()
        self._calculate_length_or_height_for_age()
        self._calculate_weight_for_age()
        super().save(*args, **kwargs)

    def _set_ages(self):
        self.age = self.child.current_age
        self.age_in_month = self.child.current_age_in_months

    def _calculate_zscore(self, standard, measurement):
        sd_minus_1 = standard.sd_minus_1
        median = standard.median
        sd_plus_1 = standard.sd_plus_1
        sd_difference = 0

        # cek apakah hasil (measurement - median) minus atau plus?
        measurement_median_difference = measurement - median
        if measurement_median_difference < 0:
            sd_difference = median - sd_minus_1
        else:
            sd_difference = sd_plus_1 - median

        z_score = (measurement - median) / sd_difference
        return z_score

    def _generate_growth_chart(
        self,
        anthopometric_standards,
        child_measurements,
        measure_type,
        chart_attr,
        title,
        ylabel,
        xlabel,
    ):
        # Create the chart
        index = np.array([])
        min_1 = np.array([])
        min_2 = np.array([])
        min_3 = np.array([])
        median = np.array([])
        pos_1 = np.array([])
        pos_2 = np.array([])
        pos_3 = np.array([])

        for row in anthopometric_standards:
            index = np.append(index, row.index)
            min_3 = np.append(min_3, row.sd_minus_3)
            min_2 = np.append(min_2, row.sd_minus_2)
            min_1 = np.append(min_1, row.sd_minus_1)
            median = np.append(median, row.median)
            pos_1 = np.append(pos_1, row.sd_plus_1)
            pos_2 = np.append(pos_2, row.sd_plus_2)
            pos_3 = np.append(pos_3, row.sd_plus_3)

        # mengatur ukuran grafik
        plt.figure(figsize=(16, 9))

        plt.plot(index.astype(int), min_3.astype(float), label="-3 SD")
        plt.plot(index.astype(int), min_2.astype(float), label="-2 SD")
        # plt.plot(index.astype(int), min_1.astype(float), label='-1 SD')
        plt.plot(index.astype(int), median.astype(float), label="Median")
        # plt.plot(index.astype(int), pos_1.astype(float), label='+1 SD')
        plt.plot(index.astype(int), pos_2.astype(float), label="+2 SD")
        plt.plot(index.astype(int), pos_3.astype(float), label="+3 SD")

        # Menambah keterangan ke Grafik
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.grid()
        plt.legend()

        # Mengatur titik koordinat pertumbuhan anak
        list_of_measure = []
        list_of_age = []

        for measurement in child_measurements:
            # untuk menghindari duplikat data pada grafik
            if (
                measurement.id == self.id
            ):  # bernilai true jika measurement sudah disimpan di database
                list_of_measure.append(getattr(self, measure_type))
                list_of_age.append(self.age_in_month)
                continue
            list_of_measure.append(getattr(measurement, measure_type))
            list_of_age.append(measurement.age_in_month)
        # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
        if not self.id:
            list_of_measure.append(self.height)
            list_of_age.append(self.age_in_month)

        # Tambahkan titik koordinat pertumbuhan anak
        plt.scatter(
            list_of_age,
            list_of_measure,
            color="red",
            label="Pertumbuhan Anak",
        )

        # Hubungkan titik koordinat dengan garis
        plt.plot(
            list_of_age,
            list_of_measure,
            color="red",
            linestyle="dashed",
        )

        # Save the figure
        figure = io.BytesIO()
        plt.savefig(figure, format="png", bbox_inches="tight")
        content_file = ImageFile(figure)

        # Hapus gambar lama
        old_chart = getattr(self.child.growthchart, chart_attr)
        if old_chart:
            old_chart.delete()

        # Simpan gambar baru
        getattr(self.child.growthchart, chart_attr).save(
            f"{self.child.id}_{chart_attr}.png", content_file
        )

        plt.close()
        figure.close()

    def _calculate_length_or_height_for_age(self):
        child_age = self.age_in_month
        gender = self.child.gender

        # get anthopometric_standards
        measurement_type = "length_for_age" if child_age <= 24 else "height_for_age"
        index_filter = {"index__lte": 24} if child_age <= 24 else {"index__gte": 25}
        anthopometric_standards = AnthropometricStandard.objects.filter(
            measurement_type=measurement_type, gender=gender, **index_filter
        )

        if not anthopometric_standards:
            raise ValueError("Length or height for age standards not found")

        # get standard data
        standard = anthopometric_standards.filter(index=child_age).first()

        # calculate z score
        z_score = self._calculate_zscore(standard=standard, measurement=self.height)

        # assign z score
        self.z_score_height_for_age = z_score

        # determine category
        if z_score < -3:
            self.height_for_age = "Sangat Pendek"
        elif -3 <= z_score < -2:
            self.height_for_age = "Pendek"
        elif -2 <= z_score < 3:
            self.height_for_age = "Normal"
        else:
            self.height_for_age = "Tinggi"

        # generate growth chart
        chart_attr = (
            "length_for_age_chart_0_24"
            if self.age_in_month <= 24
            else "height_for_age_chart_24_60"
        )
        title = (
            "Tinggi Badan Menurut Umur (0-24 Bulan)"
            if self.age_in_month <= 24
            else "Tinggi Badan Menurut Umur (24-60 Bulan)"
        )
        ylabel = "Tinggi Badan (cm)"
        xlabel = "Umur (bulan)"

        age_in_month_filter = (
            {"age_in_month__lte": 24}
            if self.age_in_month <= 24
            else {"age_in_month__gte": 25}
        )
        child_measurements = ChildMeasurement.objects.filter(
            child=self.child, **age_in_month_filter
        ).order_by("created_at")

        self._generate_growth_chart(
            anthopometric_standards=anthopometric_standards,
            child_measurements=child_measurements,
            measure_type="height",
            chart_attr=chart_attr,
            title=title,
            ylabel=ylabel,
            xlabel=xlabel,
        )

    def _calculate_weight_for_age(self):
        child_age = self.age_in_month
        gender = self.child.gender

        # get anthopometric_standards
        measurement_type = "weight_for_age"
        index_filter = {"index__lte": 24} if child_age <= 24 else {"index__gte": 25}
        anthopometric_standards = AnthropometricStandard.objects.filter(
            measurement_type=measurement_type, gender=gender, **index_filter
        )

        if not anthopometric_standards:
            raise ValueError("Weight for age standards not found")

        # get standard data
        standard = anthopometric_standards.filter(index=child_age).first()

        # calculate z score
        z_score = self._calculate_zscore(standard=standard, measurement=self.weight)

        # assign z score
        self.z_score_weight_for_age = z_score

        # determine category
        if z_score < -3:
            self.weight_for_age = "Berat badan sangat kurang"
        elif (z_score >= -3) and (z_score < -2):
            self.weight_for_age = "Berat badan kurang"
        elif (z_score >= -2) and (z_score <= 1):
            self.weight_for_age = "Berat badan normal"
        else:
            self.weight_for_age = "Resiko berat badan lebih"

        # generate growth chart
        chart_attr = (
            "weight_for_age_chart_0_24"
            if self.age_in_month <= 24
            else "weight_for_age_chart_24_60"
        )
        title = (
            "Berat Badan Menurut Umur (0-24 Bulan)"
            if self.age_in_month <= 24
            else "Berat Badan Menurut Umur (24-60 Bulan)"
        )
        ylabel = "Berat Badan (kg)"
        xlabel = "Umur (bulan)"

        age_in_month_filter = (
            {"age_in_month__lte": 24}
            if self.age_in_month <= 24
            else {"age_in_month__gte": 25}
        )
        child_measurements = ChildMeasurement.objects.filter(
            child=self.child, **age_in_month_filter
        ).order_by("created_at")

        self._generate_growth_chart(
            anthopometric_standards=anthopometric_standards,
            child_measurements=child_measurements,
            measure_type="weight",
            chart_attr=chart_attr,
            title=title,
            ylabel=ylabel,
            xlabel=xlabel,
        )
