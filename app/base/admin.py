from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from base.models import (
    Village,
    Child,
    Posyandu,
    MidwifeAssignment,
    PosyanduActivity,
    ParentPosyandu,
    ChildMeasurement,
    GrowthChart,
    CadreAssignment,

    AnthropometricStandard,

    # LengthForAgeBoys,
    # LengthForAgeGirls,
    # HeightForAgeBoys,
    # HeightForAgeGirls,
)


class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'current_age',
                    'curent_age_in_months')


class PosyanduAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'village', 'address')


class ChildMeasurementAdmin(admin.ModelAdmin):
    list_display = ("child", "age", "age_in_month", "weight", "height", "height_for_age",
                    "z_score_height_for_age", "weight_for_age", "z_score_weight_for_age")


class PosyanduActivityAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


class AnthropometricStandardAdmin(admin.ModelAdmin):
    search_fields = ("index", "measurement_type",)


admin.site.register(Village)
admin.site.register(Child, ChildAdmin)
admin.site.register(Posyandu, PosyanduAdmin)
admin.site.register(MidwifeAssignment)
admin.site.register(PosyanduActivity, PosyanduActivityAdmin)
admin.site.register(ParentPosyandu)
admin.site.register(ChildMeasurement, ChildMeasurementAdmin)
admin.site.register(GrowthChart)
admin.site.register(CadreAssignment)

admin.site.register(AnthropometricStandard, AnthropometricStandardAdmin)

# admin.site.register(LengthForAgeBoys)
# admin.site.register(LengthForAgeGirls)
# admin.site.register(HeightForAgeBoys)
# admin.site.register(HeightForAgeGirls)

# Customizing Django Admin
admin.site.site_header = _("Posyandu Admin")
admin.site.site_title = _("Posyandu Admin")
admin.site.index_title = _("Selamat Datang di Admin Posyandu")
