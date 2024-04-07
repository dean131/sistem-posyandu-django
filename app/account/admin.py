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
)


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "role", "is_registered",]
    class Meta:
        model = User


class ParentAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "role", "is_registered",]
    class Meta:
        model = Parent


class MidwifeAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "role", "is_registered",]
    class Meta:
        model = Midwife


class CadreAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "role", "is_registered",]
    class Meta:
        model = Cadre


class PuskesmasAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "role", "is_registered",]
    class Meta:
        model = Puskesmas


class OTPAdmin(admin.ModelAdmin):
    list_display = ["user", "otp"]
    class Meta:
        model = OTP
        

# Entities
admin.site.register(User, UserAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Midwife, MidwifeAdmin)
admin.site.register(Cadre, CadreAdmin)
admin.site.register(Puskesmas, PuskesmasAdmin)
admin.site.register(OTP, OTPAdmin)
# Profiles
admin.site.register(ParentProfile)
admin.site.register(MidwifeProfile)
admin.site.register(CadreProfile)
admin.site.register(PuskesmasProfile)
