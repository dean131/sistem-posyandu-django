from calendar import c
from django.contrib import admin

from .models import (
    User,
    Parent,
    Midwife,
    Cadre,
    Puskesmas,
    OTP,
    ParentProfile,
    MidwifeProfile,
    CadreProfile,
    PuskesmasProfile,
    Address,
)


class UserAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in User._meta.fields]


class ParentAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Parent._meta.fields]


class MidwifeAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Midwife._meta.fields]


class CadreAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Cadre._meta.fields]


class PuskesmasAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Puskesmas._meta.fields]


class OTPAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OTP._meta.fields]


class AddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Address._meta.fields]


class ParentProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ParentProfile._meta.fields]


class MidwifeProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MidwifeProfile._meta.fields]


class CadreProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CadreProfile._meta.fields]


class PuskesmasProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PuskesmasProfile._meta.fields]


# Entities
admin.site.register(User, UserAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Midwife, MidwifeAdmin)
admin.site.register(Cadre, CadreAdmin)
admin.site.register(Puskesmas, PuskesmasAdmin)
admin.site.register(OTP, OTPAdmin)
# Profiles
admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(MidwifeProfile, MidwifeProfileAdmin)
admin.site.register(CadreProfile, CadreProfileAdmin)
admin.site.register(PuskesmasProfile, PuskesmasProfileAdmin)
# Address
admin.site.register(Address, AddressAdmin)
