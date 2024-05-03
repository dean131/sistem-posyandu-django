from django.contrib import admin


from base.models import (
    Village,
    Child,
    Posyandu,
    MidwifeAssignment,
    PosyanduActivity,
    ParentPosyandu,
    ChildMeasurement,
    LengthForAgeBoys,
    LengthForAgeGirls,
    HeightForAgeBoys,
    HeightForAgeGirls,
    GrowthChart,
    CadreAssignment
)


class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'current_age', 'curent_age_in_months')

class PosyanduAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'village', 'address')

class ChildMeasurementAdmin(admin.ModelAdmin):
    list_display = ("child", "age", "age_in_month", "weight", "height", "height_for_age", "z_score_height_for_age")

admin.site.register(Village) 
admin.site.register(Child, ChildAdmin)   
admin.site.register(Posyandu, PosyanduAdmin)
admin.site.register(MidwifeAssignment)
admin.site.register(PosyanduActivity)
admin.site.register(ParentPosyandu)
admin.site.register(ChildMeasurement, ChildMeasurementAdmin)
admin.site.register(LengthForAgeBoys)
admin.site.register(LengthForAgeGirls)
admin.site.register(HeightForAgeBoys)
admin.site.register(HeightForAgeGirls)
admin.site.register(GrowthChart)
admin.site.register(CadreAssignment)
