from django.contrib import admin

from .models import (
    User, 
    Parent, 
    Midwife, 
    Cadre,
    OTP
)

class OTPAdmin(admin.ModelAdmin):
    list_display = ["user", "otp"]
    class Meta:
        model = OTP
        

# Register your models here.
admin.site.register(User)
admin.site.register(Parent)
admin.site.register(Midwife)
admin.site.register(Cadre)
admin.site.register(OTP, OTPAdmin)
