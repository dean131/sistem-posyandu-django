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
)


class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'current_age')

class PosyanduAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'village', 'address')

admin.site.register(Village) 
admin.site.register(Child, ChildAdmin)   
admin.site.register(Posyandu, PosyanduAdmin)
admin.site.register(MidwifeAssignment)
admin.site.register(PosyanduActivity)
admin.site.register(ParentPosyandu)
admin.site.register(ChildMeasurement)
admin.site.register(LengthForAgeBoys)
admin.site.register(LengthForAgeGirls)
