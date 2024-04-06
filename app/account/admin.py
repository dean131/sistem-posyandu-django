from django.contrib import admin

from .models import (
    User, 
    Parent, 
    Midwife, 
    Cadre,
    OTP,

    ParentProfile,
    MidwifeProfile,
    CadreProfile,
    PuskesmasProfile,
)

class OTPAdmin(admin.ModelAdmin):
    list_display = ["user", "otp"]
    class Meta:
        model = OTP
        

# Entities
admin.site.register(User)
admin.site.register(Parent)
admin.site.register(Midwife)
admin.site.register(Cadre)
admin.site.register(OTP, OTPAdmin)
# Profiles
admin.site.register(ParentProfile)
admin.site.register(MidwifeProfile)
admin.site.register(CadreProfile)
admin.site.register(PuskesmasProfile)
