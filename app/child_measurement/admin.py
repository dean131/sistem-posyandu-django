from django.contrib import admin
from .models import ChildMeasurement, GrowthChart, AnthropometricStandard


# Register your models here.
class ChildMeasurementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChildMeasurement._meta.fields]


class GrowthChartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GrowthChart._meta.fields]


class AnthropometricStandardAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AnthropometricStandard._meta.fields]


admin.site.register(ChildMeasurement, ChildMeasurementAdmin)
admin.site.register(GrowthChart, GrowthChartAdmin)
admin.site.register(AnthropometricStandard, AnthropometricStandardAdmin)
