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
            self.set_ages()
        self.calculate_length_and_height_for_age()
        super().save(*args, **kwargs)

    def set_ages(self):
        self.age = self.child.current_age
        self.age_in_month = self.child.current_age_in_months

    def calculate_length_and_height_for_age(self):
        def get_queryset_length_for_age(gender, child_age):
            measurement_type = "length_for_age" if child_age < 24 else "height_for_age"
            index_filter = {"index__lte": 24} if child_age < 24 else {"index__gte": 25}
            return AnthropometricStandard.objects.filter(
                measurement_type=measurement_type, gender=gender, **index_filter
            )

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
        sd = queryset.filter(index=child_age).first()
        height = self.height
        median = sd.median
        height_median_difference = height - median
        sd_difference = determine_sd_difference_length_for_age(sd=sd)
        # calculate z score
        z_score = height_median_difference / sd_difference
        # determine height for age z score
        self.z_score_height_for_age = z_score
        # determine height for age category
        if z_score < -3:
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
            age = np.append(age, row.index)
            min_3 = np.append(min_3, row.sd_minus_3)
            min_2 = np.append(min_2, row.sd_minus_2)
            min_1 = np.append(min_1, row.sd_minus_1)
            median = np.append(median, row.median)
            pos_1 = np.append(pos_1, row.sd_plus_1)
            pos_2 = np.append(pos_2, row.sd_plus_2)
            pos_3 = np.append(pos_3, row.sd_plus_3)

        # mengatur ukuran grafik
        plt.figure(figsize=(10, 5))

        plt.plot(age.astype(int), min_3.astype(float), label="-3 SD")
        plt.plot(age.astype(int), min_2.astype(float), label="-2 SD")
        # plt.plot(age.astype(int), min_1.astype(float), label='-1 SD')
        plt.plot(age.astype(int), median.astype(float), label="Median")
        # plt.plot(age.astype(int), pos_1.astype(float), label='+1 SD')
        plt.plot(age.astype(int), pos_2.astype(float), label="+2 SD")
        plt.plot(age.astype(int), pos_3.astype(float), label="+3 SD")

        # Menambah keterangan ke Grafik
        plt.title("Tinggi Badan Menurut Umur (TB/U)")
        plt.ylabel("Tinggi Badan (cm)")
        plt.xlabel("Umur (bulan)")
        plt.grid()
        plt.legend()

        # jika anak berumur < 24 bulan maka simpan grafik panjang badan
        # jika anak berumur >= 24 bulan maka simpan grafik tinggi badan
        if self.age_in_month < 24:
            # get child measurements history
            measurements = ChildMeasurement.objects.filter(
                child=self.child, age_in_month__lte=24
            ).order_by("created_at")
            measure_height_for_age_history = []
            measure_age_history = []

            for measurement in measurements:
                # untuk menghindari duplikat data pada grafik
                if (
                    measurement.id == self.id
                ):  # bernilai true jika measurement sudah disimpan di database
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
            plt.scatter(
                measure_age_history,
                measure_height_for_age_history,
                color="red",
                label="Pertumbuhan Anak",
            )
            # Hubungkan titik koordinat dengan garis
            plt.plot(
                measure_age_history,
                measure_height_for_age_history,
                color="red",
                linestyle="dashed",
            )

            # Save the figure
            figure = io.BytesIO()
            plt.savefig(figure, format="png")
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.length_for_age_chart_0_24:
                self.child.growthchart.length_for_age_chart_0_24.delete()
            # save new image
            self.child.growthchart.length_for_age_chart_0_24.save(
                f"{self.child.id}_length_for_age_chart_0_24.png", content_file
            )
            plt.close()
            figure.close()
        else:
            # get child measurements history
            measurements = ChildMeasurement.objects.filter(
                child=self.child, age_in_month__gte=24
            ).order_by("created_at")
            measure_height_for_age_history = []
            measure_age_history = []

            for measurement in measurements:
                # untuk menghindari duplikat data pada grafik
                if (
                    measurement.id == self.id
                ):  # bernilai true jika measurement sudah disimpan di database
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
            plt.scatter(
                measure_age_history,
                measure_height_for_age_history,
                color="red",
                label="Pertumbuhan Anak",
            )
            # Hubungkan titik koordinat dengan garis
            plt.plot(
                measure_age_history,
                measure_height_for_age_history,
                color="red",
                linestyle="dashed",
            )

            # Save the figure
            figure = io.BytesIO()
            plt.savefig(figure, format="png")
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.height_for_age_chart_24_60:
                self.child.growthchart.height_for_age_chart_24_60.delete()

            # save new image
            self.child.growthchart.height_for_age_chart_24_60.save(
                f"{self.child.id}_height_for_age_chart_24_60.png", content_file
            )
            plt.close()
            figure.close()

    def calculate_weight_for_age(self):
        def get_queryset_weight_for_age(gender, child_age):
            if gender == "M":
                if child_age < 24:
                    queryset = WeightForAgeBoys.objects.filter(index__lt=24)
                else:
                    queryset = WeightForAgeBoys.objects.filter(index__gte=24)
            else:
                if child_age < 24:
                    queryset = WeightForAgeGirls.objects.filter(index__lt=24)
                else:
                    queryset = WeightForAgeGirls.objects.filter(index__gte=24)
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
        sd = queryset.filter(index=child_age).first()
        median = sd.median
        weight_median_difference = weight - median
        sd_difference = determine_sd_difference_weight_for_age(sd=sd)
        # calculate z score
        z_score = weight_median_difference / sd_difference
        # determine weight for age z score
        self.z_score_weight_for_age = z_score
        # determine weight for age category
        if z_score < -3:
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
            age = np.append(age, row.index)
            min_3 = np.append(min_3, row.sd_minus_3)
            min_2 = np.append(min_2, row.sd_minus_2)
            min_1 = np.append(min_1, row.sd_minus_1)
            median = np.append(median, row.median)
            pos_1 = np.append(pos_1, row.sd_plus_1)
            pos_2 = np.append(pos_2, row.sd_plus_2)
            pos_3 = np.append(pos_3, row.sd_plus_3)

        # mengatur ukuran grafik
        plt.figure(figsize=(10, 5))

        plt.plot(age.astype(int), min_3.astype(float), label="-3 SD")
        plt.plot(age.astype(int), min_2.astype(float), label="-2 SD")
        # plt.plot(age.astype(int), min_1.astype(float), label='-1 SD')
        plt.plot(age.astype(int), median.astype(float), label="Median")
        # plt.plot(age.astype(int), pos_1.astype(float), label='+1 SD')
        plt.plot(age.astype(int), pos_2.astype(float), label="+2 SD")
        plt.plot(age.astype(int), pos_3.astype(float), label="+3 SD")

        # Menambah keterangan ke Grafik
        plt.title(sd.title)
        plt.ylabel(sd.ylabel)
        plt.xlabel(sd.xlabel)
        plt.grid()
        plt.legend()

        if self.age_in_month < 24:
            # get child measurements history
            measurements = ChildMeasurement.objects.filter(
                child=self.child, age_in_month__lte=24
            ).order_by("created_at")
        else:
            # get child measurements history
            measurements = ChildMeasurement.objects.filter(
                child=self.child, age_in_month__gte=24
            ).order_by("created_at")

        measure_weight_for_age_history = []
        measure_age_history = []

        for measurement in measurements:
            # untuk menghindari duplikat data pada grafik
            if (
                measurement.id == self.id
            ):  # bernilai true jika measurement sudah disimpan di database
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
        plt.scatter(
            measure_age_history,
            measure_weight_for_age_history,
            color="red",
            label="Pertumbuhan Anak",
        )
        # Hubungkan titik koordinat dengan garis
        plt.plot(
            measure_age_history,
            measure_weight_for_age_history,
            color="red",
            linestyle="dashed",
        )

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
            plt.savefig(figure, format="png")
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.weight_for_age_chart_0_24:
                self.child.growthchart.weight_for_age_chart_0_24.delete()
            # save new image
            self.child.growthchart.weight_for_age_chart_0_24.save(
                f"{self.child.id}_weight_for_age_chart_0_24.png", content_file
            )
            plt.close()
            figure.close()
        else:
            # Save the figure
            figure = io.BytesIO()
            plt.savefig(figure, format="png")
            content_file = ImageFile(figure)

            # delete old image
            if self.child.growthchart.weight_for_age_chart_24_60:
                self.child.growthchart.weight_for_age_chart_24_60.delete()
            # save new image
            self.child.growthchart.weight_for_age_chart_24_60.save(
                f"{self.child.id}_weight_for_age_chart_24_60.png", content_file
            )
            plt.close()
            figure.close()


# class ChildMeasurement(models.Model):
#     """
#     Merepresentasikan pengukuran seorang Anak.
#     """

#     MEASUREMENT_METHOD_CHOICES = [
#         ("STANDING", "Standing"),
#         ("SUPINE", "Supine"),
#     ]

#     WEIGHT_GAIN_CHOICES = [("O", "O"), ("T", "T")]

#     weight = models.FloatField()
#     height = models.FloatField()
#     head_circumference = models.FloatField(null=True, blank=True)
#     # cara ukur
#     measurement_method = models.CharField(
#         max_length=8, choices=MEASUREMENT_METHOD_CHOICES, null=True
#     )
#     # usia saat pengukuran dalam tahun, bulan, hari
#     age = models.CharField(max_length=50, null=True, blank=True)
#     # usia dalam bulan
#     age_in_month = models.PositiveIntegerField(null=True, blank=True)
#     # lingkar lengan atas / lila
#     # arm_circumference = models.FloatField(null=True, blank=True)
#     # bb/u
#     weight_for_age = models.CharField(
#         max_length=30, null=True, blank=True, default="normal"
#     )
#     # z score bb/u
#     z_score_weight_for_age = models.FloatField(null=True, blank=True)
#     # tb/u
#     height_for_age = models.CharField(
#         max_length=30, null=True, blank=True, default="normal"
#     )
#     # z score tb/u
#     z_score_height_for_age = models.FloatField(null=True, blank=True)
#     # bb/tb
#     weight_for_height = models.CharField(
#         max_length=30, null=True, blank=True, default="normal"
#     )
#     # z score bb/tb
#     z_score_weight_for_height = models.FloatField(null=True, blank=True)
#     # naik berat badan
#     weight_gain = models.FloatField(null=True, blank=True)
#     # naik tinggi badan
#     height_gain = models.FloatField(null=True, blank=True)
#     # imt/u
#     bmi_for_age = models.CharField(
#         max_length=30, null=True, blank=True, default="normal"
#     )
#     # z score imt/u
#     z_score_bmi_for_age = models.FloatField(null=True, blank=True)

#     # pmt diterima (kg)
#     # pmt_received = models.FloatField(blank=True, null=True)
#     # jumlah vitamin A
#     # vitamin_a_count = models.PositiveIntegerField(blank=True, null=True)
#     # kpsp
#     # kpsp = models.BooleanField(blank=True, null=True)
#     # kia
#     # kia = models.BooleanField(blank=True, null=True)
#     # Time Fields
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # Foreign Keys
#     child = models.ForeignKey(Child, on_delete=models.CASCADE)
#     posyandu_activity = models.ForeignKey(
#         PosyanduActivity, on_delete=models.CASCADE, null=True, blank=True
#     )

#     class Meta:
#         ordering = ["-age_in_month"]

#     def __str__(self):
#         return f"Pengukuran Anak {self.child.full_name}"

#     # def save(self, *args, **kwargs):
#     #     if not self.id:
#     #         self.set_ages()  # set umur sebelum dilakukan perhitungan
#     #     match self.child.gender:
#     #         case "M":
#     #             if self.age_in_month < 24:
#     #                 # WEIGHT FOR AGE
#     #                 self.calculate_weight_for_age_with_param(
#     #                     measurement_type="m_weight_for_age",
#     #                     chart_attr="weight_for_age_0_24_chart",
#     #                     title="Berat Badan Menurut Umur Laki-laki (0-24 Bulan)"
#     #                 )
#     #                 # LENGTH FOR AGE
#     #                 self.calculate_length_or_height_for_age_with_param(
#     #                     measurement_type="m_length_for_age",
#     #                     chart_attr="length_for_age_chart",
#     #                     title="Tinggi Badan Menurut Umur Laki-laki (0-24 Bulan)"
#     #                 )
#     #             else:
#     #                 # WEIGHT FOR AGE
#     #                 self.calculate_weight_for_age_with_param(
#     #                     measurement_type="m_weight_for_age",
#     #                     chart_attr="weight_for_age_24_60_chart",
#     #                     title="Berat Badan Menurut Umur Laki-laki (24-60 Bulan)"
#     #                 )
#     #                 # HEIGHT FOR AGE
#     #                 self.calculate_length_or_height_for_age_with_param(
#     #                     measurement_type="m_height_for_age",
#     #                     chart_attr="height_for_age_chart",
#     #                     title="Tinggi Badan Menurut Umur Laki-laki (24-60 Bulan)"
#     #                 )
#     #         case "F":
#     #             if self.age_in_month < 24:
#     #                 # WEIGHT FOR AGE
#     #                 self.calculate_weight_for_age_with_param(
#     #                     measurement_type="f_weight_for_age",
#     #                     chart_attr="weight_for_age_0_24_chart",
#     #                     title="Berat Badan Menurut Umur Perempuan (0-24 Bulan)"
#     #                 )
#     #                 # LENGTH FOR AGE
#     #                 self.calculate_length_or_height_for_age_with_param(
#     #                     measurement_type="f_length_for_age",
#     #                     chart_attr="length_for_age_chart",
#     #                     title="Tinggi Badan Menurut Umur Perempuan (0-24 Bulan)"
#     #                 )
#     #             else:
#     #                 # WEIGHT FOR AGE
#     #                 self.calculate_weight_for_age_with_param(
#     #                     measurement_type="f_weight_for_age",
#     #                     chart_attr="weight_for_age_24_60_chart",
#     #                     title="Berat Badan Menurut Umur Perempuan (24-60 Bulan)"
#     #                 )
#     #                 # HEIGHT FOR AGE
#     #                 self.calculate_length_or_height_for_age_with_param(
#     #                     measurement_type="f_height_for_age",
#     #                     chart_attr="height_for_age_chart",
#     #                     title="Tinggi Badan Menurut Umur Perempuan (24-60 Bulan)"
#     #                 )

#     #     # self.calculate_length_and_height_for_age()
#     #     super().save(*args, **kwargs)

#     def set_ages(self):
#         self.age = self.child.current_age
#         self.age_in_month = self.child.curent_age_in_months

#     def calculate_zscore(self, SD):
#         weight_median_difference = self.weight - SD.median
#         sd_difference = (
#             (SD.median - SD.sd_minus_1)
#             if weight_median_difference < 0
#             else (SD.sd_plus_1 - SD.median)
#         )
#         z_score = weight_median_difference / sd_difference
#         print("\n" + "=" * 50)
#         print(SD)
#         print(f"INDEX: {SD.index}")
#         print(f"SD_MIN_1: {SD.sd_minus_1}")
#         print(f"MEDIAN: {SD.median}")
#         print(f"SD_PLUS_1: {SD.sd_plus_1}")
#         print(f"SD DIFFERENCE: {sd_difference}")
#         print(f"Z-SCORE: {z_score}")
#         print("=" * 50 + "\n")
#         return z_score

#     def calculate_weight_for_age_with_param(self, measurement_type, chart_attr, title):
#         # Determine the queryset based on age limit and measurement type
#         if self.age_in_month < 24:
#             queryset = AnthropometricStandard.objects.filter(
#                 index__lt=24, measurement_type=measurement_type
#             )
#         else:
#             queryset = AnthropometricStandard.objects.filter(
#                 index__gte=24, measurement_type=measurement_type
#             )

#         # Determine standard deviation
#         SD = queryset.filter(index=self.age_in_month).first()

#         # Calculate z-score
#         self.z_score_weight_for_age = self.calculate_zscore(SD=SD)

#         # Determine nutritional status
#         self.weight_for_age = (
#             "Berat badan sangat kurang"
#             if self.z_score_weight_for_age < -3
#             else (
#                 "Berat badan kurang"
#                 if -3 <= self.z_score_weight_for_age < -2
#                 else (
#                     "Berat badan normal"
#                     if -2 <= self.z_score_weight_for_age <= 1
#                     else "Resiko berat badan lebih"
#                 )
#             )
#         )

#         # Create the chart data arrays
#         index = np.array([])
#         min_1 = np.array([])
#         min_2 = np.array([])
#         min_3 = np.array([])
#         median = np.array([])
#         pos_1 = np.array([])
#         pos_2 = np.array([])
#         pos_3 = np.array([])

#         for row in queryset:
#             index = np.append(index, row.index)
#             min_3 = np.append(min_3, row.sd_minus_3)
#             min_2 = np.append(min_2, row.sd_minus_2)
#             min_1 = np.append(min_1, row.sd_minus_1)
#             median = np.append(median, row.median)
#             pos_1 = np.append(pos_1, row.sd_plus_1)
#             pos_2 = np.append(pos_2, row.sd_plus_2)
#             pos_3 = np.append(pos_3, row.sd_plus_3)

#         # Set up the plot
#         plt.figure(figsize=(10, 5))
#         plt.plot(index.astype(float), min_3.astype(float), label="-3 SD")
#         plt.plot(index.astype(float), min_2.astype(float), label="-2 SD")
#         plt.plot(index.astype(float), min_1.astype(float), label="-1 SD")
#         plt.plot(index.astype(float), median.astype(float), label="Median")
#         plt.plot(index.astype(float), pos_1.astype(float), label="+1 SD")
#         plt.plot(index.astype(float), pos_2.astype(float), label="+2 SD")
#         plt.plot(index.astype(float), pos_3.astype(float), label="+3 SD")
#         plt.title(title)
#         plt.ylabel("Berat Badan (kg)")
#         plt.xlabel("Umur (bulan)")
#         plt.grid()
#         plt.legend()

#         # Get child measurements history
#         measurements = (
#             ChildMeasurement.objects.filter(
#                 child=self.child, age_in_month__lt=24
#             ).order_by("created_at")
#             if self.age_in_month < 24
#             else ChildMeasurement.objects.filter(
#                 child=self.child, age_in_month__gte=24
#             ).order_by("created_at")
#         )

#         measurements_history, measure_age_history = [], []

#         for measurement in measurements:
#             if measurement.id == self.id:
#                 measurements_history.append(self.weight)
#                 measure_age_history.append(self.age_in_month)
#                 continue
#             measurements_history.append(measurement.weight)
#             measure_age_history.append(measurement.age_in_month)

#         if not self.id:
#             measurements_history.append(self.weight)
#             measure_age_history.append(self.age_in_month)

#         plt.scatter(
#             measure_age_history,
#             measurements_history,
#             color="red",
#             label="Pertumbuhan Anak",
#         )
#         plt.plot(
#             measure_age_history, measurements_history, color="red", linestyle="dashed"
#         )

#         # Save the figure
#         figure = io.BytesIO()
#         plt.savefig(figure, format="png")
#         content_file = ImageFile(figure)

#         # Delete old image if exists
#         old_image = getattr(self.child.growthchart, chart_attr)
#         if old_image:
#             old_image.delete()

#         # Save new image
#         getattr(self.child.growthchart, chart_attr).save(
#             f"{self.child.id}_{chart_attr}.png", content_file
#         )
#         plt.close()
#         figure.close()

#     def calculate_length_or_height_for_age_with_param(
#         self, measurement_type, chart_attr, title
#     ):
#         # Determine the queryset based on age limit and measurement type
#         if self.age_in_month < 24:
#             queryset = AnthropometricStandard.objects.filter(
#                 index__lt=24, measurement_type=measurement_type
#             )
#         else:
#             queryset = AnthropometricStandard.objects.filter(
#                 index__gte=24, measurement_type=measurement_type
#             )
#         print(f"QUERYSET: {queryset}")
#         # Determine standard deviation
#         SD = queryset.filter(index=self.age_in_month).first()

#         print(f"SD HEIGHT FOR AGE: {SD}")

#         # Calculate z-score
#         self.z_score_height_for_age = self.calculate_zscore(SD=SD)

#         self.height_for_age = (
#             "Sangat pendek"
#             if self.z_score_height_for_age < -3
#             else (
#                 "Pendek"
#                 if -3 <= self.z_score_height_for_age < -2
#                 else "Normal" if -2 <= self.z_score_height_for_age <= 3 else "Tinggi"
#             )
#         )

#         # Create the chart data arrays
#         index = np.array([])
#         min_1 = np.array([])
#         min_2 = np.array([])
#         min_3 = np.array([])
#         median = np.array([])
#         pos_1 = np.array([])
#         pos_2 = np.array([])
#         pos_3 = np.array([])

#         for row in queryset:
#             index = np.append(index, row.index)
#             min_3 = np.append(min_3, row.sd_minus_3)
#             min_2 = np.append(min_2, row.sd_minus_2)
#             min_1 = np.append(min_1, row.sd_minus_1)
#             median = np.append(median, row.median)
#             pos_1 = np.append(pos_1, row.sd_plus_1)
#             pos_2 = np.append(pos_2, row.sd_plus_2)
#             pos_3 = np.append(pos_3, row.sd_plus_3)

#         # Set up the plot
#         plt.figure(figsize=(10, 5))
#         plt.plot(index.astype(float), min_3.astype(float), label="-3 SD")
#         plt.plot(index.astype(float), min_2.astype(float), label="-2 SD")
#         plt.plot(index.astype(float), min_1.astype(float), label="-1 SD")
#         plt.plot(index.astype(float), median.astype(float), label="Median")
#         plt.plot(index.astype(float), pos_1.astype(float), label="+1 SD")
#         plt.plot(index.astype(float), pos_2.astype(float), label="+2 SD")
#         plt.plot(index.astype(float), pos_3.astype(float), label="+3 SD")
#         plt.title(title)
#         plt.ylabel("Panjang Badan (cm)")
#         plt.xlabel("Umur (bulan)")
#         plt.grid()
#         plt.legend()

#         # Get child measurements history
#         measurements = (
#             ChildMeasurement.objects.filter(
#                 child=self.child, age_in_month__lt=24
#             ).order_by("created_at")
#             if self.age_in_month < 24
#             else ChildMeasurement.objects.filter(
#                 child=self.child, age_in_month__gte=24
#             ).order_by("created_at")
#         )

#         measurements_history, measure_age_history = [], []

#         for measurement in measurements:
#             if measurement.id == self.id:
#                 measurements_history.append(self.height)
#                 measure_age_history.append(self.age_in_month)
#                 continue
#             measurements_history.append(measurement.height)
#             measure_age_history.append(measurement.age_in_month)

#         if not self.id:
#             measurements_history.append(self.height)
#             measure_age_history.append(self.age_in_month)

#         plt.scatter(
#             measure_age_history,
#             measurements_history,
#             color="red",
#             label="Pertumbuhan Anak",
#         )
#         plt.plot(
#             measure_age_history, measurements_history, color="red", linestyle="dashed"
#         )

#         # Save the figure
#         figure = io.BytesIO()
#         plt.savefig(figure, format="png")
#         content_file = ImageFile(figure)

#         # Delete old image if exists
#         old_image = getattr(self.child.growthchart, chart_attr)
#         if old_image:
#             old_image.delete()

#         # Save new image
#         getattr(self.child.growthchart, chart_attr).save(
#             f"{self.child.id}_{chart_attr}.png", content_file
#         )
#         plt.close()
#         figure.close()

#     def calculate_male_weight_for_age_0_24(self):
#         # MENENTUKAN QUERYSET
#         queryset = AnthropometricStandard.objects.filter(
#             index__lt=24, measurement_type="m_weight_for_age"
#         )
#         # MENENTUKAN STANDARD DEVIASI
#         SD = queryset.filter(index=self.age_in_month).first()
#         # MENGHITUNG Z-SCORE
#         self.z_score_weight_for_age = self.calculate_zscore(SD=SD)

#         # Create the chart
#         index = np.array([])
#         min_1 = np.array([])
#         min_2 = np.array([])
#         min_3 = np.array([])
#         median = np.array([])
#         pos_1 = np.array([])
#         pos_2 = np.array([])
#         pos_3 = np.array([])

#         for row in queryset:
#             index = np.append(index, row.index)
#             min_3 = np.append(min_3, row.sd_minus_3)
#             min_2 = np.append(min_2, row.sd_minus_2)
#             min_1 = np.append(min_1, row.sd_minus_1)
#             median = np.append(median, row.median)
#             pos_1 = np.append(pos_1, row.sd_plus_1)
#             pos_2 = np.append(pos_2, row.sd_plus_2)
#             pos_3 = np.append(pos_3, row.sd_plus_3)

#         # mengatur ukuran grafik
#         plt.figure(figsize=(10, 5))

#         plt.plot(index.astype(float), min_3.astype(float), label="-3 SD")
#         plt.plot(index.astype(float), min_2.astype(float), label="-2 SD")
#         plt.plot(index.astype(float), min_1.astype(float), label="-1 SD")
#         plt.plot(index.astype(float), median.astype(float), label="Median")
#         plt.plot(index.astype(float), pos_1.astype(float), label="+1 SD")
#         plt.plot(index.astype(float), pos_2.astype(float), label="+2 SD")
#         plt.plot(index.astype(float), pos_3.astype(float), label="+3 SD")

#         # Menambah keterangan ke Grafik
#         plt.title("Berat Badan Menurut Umur (0-24 Bulan)")
#         plt.ylabel("Panjang Badan (cm)")
#         plt.xlabel("Umur (bulan)")
#         plt.grid()
#         plt.legend()

#         # MEAMBAHKKAN TITIK KOORDINAT PERTUMBUHAN ANAK
#         # get child measurements history
#         measurements = ChildMeasurement.objects.filter(
#             child=self.child, age_in_month__lt=24
#         ).order_by("created_at")

#         measurements_history = []
#         measure_age_history = []

#         for measurement in measurements:
#             # untuk menghindari duplikat data pada grafik
#             if (
#                 measurement.id == self.id
#             ):  # bernilai true jika measurement sudah disimpan di database
#                 measurements_history.append(self.weight)
#                 measure_age_history.append(self.age_in_month)
#                 continue
#             measurements_history.append(measurement.weight)
#             measure_age_history.append(measurement.age_in_month)
#         # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
#         if not self.id:
#             measurements_history.append(self.weight)
#             measure_age_history.append(self.age_in_month)

#         # Tambahkan titik koordinat pertumbuhan anak
#         plt.scatter(
#             measure_age_history,
#             measurements_history,
#             color="red",
#             label="Pertumbuhan Anak",
#         )
#         # Hubungkan titik koordinat dengan garis
#         plt.plot(
#             measure_age_history, measurements_history, color="red", linestyle="dashed"
#         )

#         # # step ticks for x axis
#         # min_age = int(age.min())
#         # max_age = int(age.max()+1)
#         # plt.xticks(range(min_age, max_age))

#         # # step ticks for y axis
#         # min_weight = int(min_3.min())
#         # max_weight = int(pos_3.max()+1)
#         # plt.yticks(range(min_weight, max_weight))

#         # Save the figure
#         figure = io.BytesIO()
#         plt.savefig(figure, format="png")
#         content_file = ImageFile(figure)

#         # delete old image
#         if self.child.growthchart.weight_for_age_0_24_chart:
#             self.child.growthchart.weight_for_age_0_24_chart.delete()
#         # save new image
#         self.child.growthchart.weight_for_age_0_24_chart.save(
#             f"{self.child.id}_weight_for_age_0_24_chart.png", content_file
#         )
#         plt.close()
#         figure.close()

#     def calculate_male_weight_for_age_24_60(self):
#         # MENENTUKAN QUERYSET
#         queryset = AnthropometricStandard.objects.filter(
#             index__gte=24, measurement_type="m_weight_for_age"
#         )
#         # MENENTUKAN STANDARD DEVIASI
#         SD = queryset.filter(index=self.age_in_month).first()
#         # MENGHITUNG Z-SCORE
#         self.z_score_weight_for_age = self.calculate_zscore(SD=SD)
#         # MENENTUKAN STATUS GIZI
#         self.weight_for_age = (
#             "Berat badan sangat kurang"
#             if self.z_score_weight_for_age < -3
#             else (
#                 "Berat badan kurang"
#                 if -3 <= self.z_score_weight_for_age < -2
#                 else (
#                     "Berat badan normal"
#                     if -2 <= self.z_score_weight_for_age <= 1
#                     else "Resiko berat badan lebih"
#                 )
#             )
#         )

#         # Create the chart
#         index = np.array([])
#         min_1 = np.array([])
#         min_2 = np.array([])
#         min_3 = np.array([])
#         median = np.array([])
#         pos_1 = np.array([])
#         pos_2 = np.array([])
#         pos_3 = np.array([])

#         for row in queryset:
#             index = np.append(index, row.index)
#             min_3 = np.append(min_3, row.sd_minus_3)
#             min_2 = np.append(min_2, row.sd_minus_2)
#             min_1 = np.append(min_1, row.sd_minus_1)
#             median = np.append(median, row.median)
#             pos_1 = np.append(pos_1, row.sd_plus_1)
#             pos_2 = np.append(pos_2, row.sd_plus_2)
#             pos_3 = np.append(pos_3, row.sd_plus_3)

#         # mengatur ukuran grafik
#         plt.figure(figsize=(10, 5))

#         plt.plot(index.astype(float), min_3.astype(float), label="-3 SD")
#         plt.plot(index.astype(float), min_2.astype(float), label="-2 SD")
#         plt.plot(index.astype(float), min_1.astype(float), label="-1 SD")
#         plt.plot(index.astype(float), median.astype(float), label="Median")
#         plt.plot(index.astype(float), pos_1.astype(float), label="+1 SD")
#         plt.plot(index.astype(float), pos_2.astype(float), label="+2 SD")
#         plt.plot(index.astype(float), pos_3.astype(float), label="+3 SD")

#         # Menambah keterangan ke Grafik
#         plt.title("Berat Badan Menurut Umur (24-60 Bulan)")
#         plt.ylabel("Panjang Badan (cm)")
#         plt.xlabel("Umur (bulan)")
#         plt.grid()
#         plt.legend()

#         # MEAMBAHKKAN TITIK KOORDINAT PERTUMBUHAN ANAK
#         # get child measurements history
#         measurements = ChildMeasurement.objects.filter(
#             child=self.child, age_in_month__gte=24
#         ).order_by("created_at")

#         measurements_history = []
#         measure_age_history = []

#         for measurement in measurements:
#             # untuk menghindari duplikat data pada grafik
#             if (
#                 measurement.id == self.id
#             ):  # bernilai true jika measurement sudah disimpan di database
#                 measurements_history.append(self.weight)
#                 measure_age_history.append(self.age_in_month)
#                 continue
#             measurements_history.append(measurement.weight)
#             measure_age_history.append(measurement.age_in_month)
#         # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
#         if not self.id:
#             measurements_history.append(self.weight)
#             measure_age_history.append(self.age_in_month)

#         # Tambahkan titik koordinat pertumbuhan anak
#         plt.scatter(
#             measure_age_history,
#             measurements_history,
#             color="red",
#             label="Pertumbuhan Anak",
#         )
#         # Hubungkan titik koordinat dengan garis
#         plt.plot(
#             measure_age_history, measurements_history, color="red", linestyle="dashed"
#         )

#         # # step ticks for x axis
#         # min_age = int(age.min())
#         # max_age = int(age.max()+1)
#         # plt.xticks(range(min_age, max_age))

#         # # step ticks for y axis
#         # min_weight = int(min_3.min())
#         # max_weight = int(pos_3.max()+1)
#         # plt.yticks(range(min_weight, max_weight))

#         # Save the figure
#         figure = io.BytesIO()
#         plt.savefig(figure, format="png")
#         content_file = ImageFile(figure)

#         # delete old image
#         if self.child.growthchart.weight_for_age_24_60_chart:
#             self.child.growthchart.weight_for_age_24_60_chart.delete()
#         # save new image
#         self.child.growthchart.weight_for_age_24_60_chart.save(
#             f"{self.child.id}_weight_for_age_24_60_chart.png", content_file
#         )
#         plt.close()
#         figure.close()

#     def calculate_female_weight_for_age_0_24(self):
#         # MENENTUKAN QUERYSET
#         queryset = AnthropometricStandard.objects.filter(
#             index__lt=24, measurement_type="m_weight_for_age"
#         )
#         # MENENTUKAN STANDARD DEVIASI
#         SD = queryset.filter(index=self.age_in_month).first()
#         # MENGHITUNG Z-SCORE
#         self.z_score_weight_for_age = self.calculate_zscore(SD=SD)

#         # Create the chart
#         index = np.array([])
#         min_1 = np.array([])
#         min_2 = np.array([])
#         min_3 = np.array([])
#         median = np.array([])
#         pos_1 = np.array([])
#         pos_2 = np.array([])
#         pos_3 = np.array([])

#         for row in queryset:
#             index = np.append(index, row.index)
#             min_3 = np.append(min_3, row.sd_minus_3)
#             min_2 = np.append(min_2, row.sd_minus_2)
#             min_1 = np.append(min_1, row.sd_minus_1)
#             median = np.append(median, row.median)
#             pos_1 = np.append(pos_1, row.sd_plus_1)
#             pos_2 = np.append(pos_2, row.sd_plus_2)
#             pos_3 = np.append(pos_3, row.sd_plus_3)

#         # mengatur ukuran grafik
#         plt.figure(figsize=(10, 5))

#         plt.plot(index.astype(float), min_3.astype(float), label="-3 SD")
#         plt.plot(index.astype(float), min_2.astype(float), label="-2 SD")
#         plt.plot(index.astype(float), min_1.astype(float), label="-1 SD")
#         plt.plot(index.astype(float), median.astype(float), label="Median")
#         plt.plot(index.astype(float), pos_1.astype(float), label="+1 SD")
#         plt.plot(index.astype(float), pos_2.astype(float), label="+2 SD")
#         plt.plot(index.astype(float), pos_3.astype(float), label="+3 SD")

#         # Menambah keterangan ke Grafik
#         plt.title("Berat Badan Menurut Umur (0-24 Bulan)")
#         plt.ylabel("Panjang Badan (cm)")
#         plt.xlabel("Umur (bulan)")
#         plt.grid()
#         plt.legend()

#         # MEAMBAHKKAN TITIK KOORDINAT PERTUMBUHAN ANAK
#         # get child measurements history
#         measurements = ChildMeasurement.objects.filter(
#             child=self.child, age_in_month__lt=24
#         ).order_by("created_at")

#         measurements_history = []
#         measure_age_history = []

#         for measurement in measurements:
#             # untuk menghindari duplikat data pada grafik
#             if (
#                 measurement.id == self.id
#             ):  # bernilai true jika measurement sudah disimpan di database
#                 measurements_history.append(self.weight)
#                 measure_age_history.append(self.age_in_month)
#                 continue
#             measurements_history.append(measurement.weight)
#             measure_age_history.append(measurement.age_in_month)
#         # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
#         if not self.id:
#             measurements_history.append(self.weight)
#             measure_age_history.append(self.age_in_month)

#         # Tambahkan titik koordinat pertumbuhan anak
#         plt.scatter(
#             measure_age_history,
#             measurements_history,
#             color="red",
#             label="Pertumbuhan Anak",
#         )
#         # Hubungkan titik koordinat dengan garis
#         plt.plot(
#             measure_age_history, measurements_history, color="red", linestyle="dashed"
#         )

#         # # step ticks for x axis
#         # min_age = int(age.min())
#         # max_age = int(age.max()+1)
#         # plt.xticks(range(min_age, max_age))

#         # # step ticks for y axis
#         # min_weight = int(min_3.min())
#         # max_weight = int(pos_3.max()+1)
#         # plt.yticks(range(min_weight, max_weight))

#         # Save the figure
#         figure = io.BytesIO()
#         plt.savefig(figure, format="png")
#         content_file = ImageFile(figure)

#         # delete old image
#         if self.child.growthchart.weight_for_age_0_24_chart:
#             self.child.growthchart.weight_for_age_0_24_chart.delete()
#         # save new image
#         self.child.growthchart.weight_for_age_0_24_chart.save(
#             f"{self.child.id}_weight_for_age_0_24_chart.png", content_file
#         )
#         plt.close()
#         figure.close()

#     def calculate_female_weight_for_age_24_60(self):
#         # MENENTUKAN QUERYSET
#         queryset = AnthropometricStandard.objects.filter(
#             index__gte=24, measurement_type="f_weight_for_age"
#         )
#         # MENENTUKAN STANDARD DEVIASI
#         SD = queryset.filter(index=self.age_in_month).first()
#         # MENGHITUNG Z-SCORE
#         self.z_score_weight_for_age = self.calculate_zscore(SD=SD)
#         # MENENTUKAN STATUS GIZI
#         self.weight_for_age = (
#             "Berat badan sangat kurang"
#             if self.z_score_weight_for_age < -3
#             else (
#                 "Berat badan kurang"
#                 if -3 <= self.z_score_weight_for_age < -2
#                 else (
#                     "Berat badan normal"
#                     if -2 <= self.z_score_weight_for_age <= 1
#                     else "Resiko berat badan lebih"
#                 )
#             )
#         )

#         # Create the chart
#         index = np.array([])
#         min_1 = np.array([])
#         min_2 = np.array([])
#         min_3 = np.array([])
#         median = np.array([])
#         pos_1 = np.array([])
#         pos_2 = np.array([])
#         pos_3 = np.array([])

#         for row in queryset:
#             index = np.append(index, row.index)
#             min_3 = np.append(min_3, row.sd_minus_3)
#             min_2 = np.append(min_2, row.sd_minus_2)
#             min_1 = np.append(min_1, row.sd_minus_1)
#             median = np.append(median, row.median)
#             pos_1 = np.append(pos_1, row.sd_plus_1)
#             pos_2 = np.append(pos_2, row.sd_plus_2)
#             pos_3 = np.append(pos_3, row.sd_plus_3)

#         # mengatur ukuran grafik
#         plt.figure(figsize=(10, 5))

#         plt.plot(index.astype(float), min_3.astype(float), label="-3 SD")
#         plt.plot(index.astype(float), min_2.astype(float), label="-2 SD")
#         plt.plot(index.astype(float), min_1.astype(float), label="-1 SD")
#         plt.plot(index.astype(float), median.astype(float), label="Median")
#         plt.plot(index.astype(float), pos_1.astype(float), label="+1 SD")
#         plt.plot(index.astype(float), pos_2.astype(float), label="+2 SD")
#         plt.plot(index.astype(float), pos_3.astype(float), label="+3 SD")

#         # Menambah keterangan ke Grafik
#         plt.title("Berat Badan Menurut Umur (24-60 Bulan)")
#         plt.ylabel("Panjang Badan (cm)")
#         plt.xlabel("Umur (bulan)")
#         plt.grid()
#         plt.legend()

#         # MEAMBAHKKAN TITIK KOORDINAT PERTUMBUHAN ANAK
#         # get child measurements history
#         measurements = ChildMeasurement.objects.filter(
#             child=self.child, age_in_month__gte=24
#         ).order_by("created_at")

#         measurements_history = []
#         measure_age_history = []

#         for measurement in measurements:
#             # untuk menghindari duplikat data pada grafik
#             if (
#                 measurement.id == self.id
#             ):  # bernilai true jika measurement sudah disimpan di database
#                 measurements_history.append(self.weight)
#                 measure_age_history.append(self.age_in_month)
#                 continue
#             measurements_history.append(measurement.weight)
#             measure_age_history.append(measurement.age_in_month)
#         # menambah titik kordinat pertumbuhan ketika data belum disimpan di database
#         if not self.id:
#             measurements_history.append(self.weight)
#             measure_age_history.append(self.age_in_month)

#         # Tambahkan titik koordinat pertumbuhan anak
#         plt.scatter(
#             measure_age_history,
#             measurements_history,
#             color="red",
#             label="Pertumbuhan Anak",
#         )
#         # Hubungkan titik koordinat dengan garis
#         plt.plot(
#             measure_age_history, measurements_history, color="red", linestyle="dashed"
#         )

#         # # step ticks for x axis
#         # min_age = int(age.min())
#         # max_age = int(age.max()+1)
#         # plt.xticks(range(min_age, max_age))

#         # # step ticks for y axis
#         # min_weight = int(min_3.min())
#         # max_weight = int(pos_3.max()+1)
#         # plt.yticks(range(min_weight, max_weight))

#         # Save the figure
#         figure = io.BytesIO()
#         plt.savefig(figure, format="png")
#         content_file = ImageFile(figure)

#         # delete old image
#         if self.child.growthchart.weight_for_age_24_60_chart:
#             self.child.growthchart.weight_for_age_24_60_chart.delete()
#         # save new image
#         self.child.growthchart.weight_for_age_24_60_chart.save(
#             f"{self.child.id}_weight_for_age_24_60_chart.png", content_file
#         )
#         plt.close()
#         figure.close()
