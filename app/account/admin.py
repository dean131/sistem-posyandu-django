from django.contrib import admin

from .models import (
    User, 
    Parent, 
    Midwife, 
    Cadre,
    OTP
)

# Register your models here.
admin.site.register(User)
admin.site.register(Parent)
admin.site.register(Midwife)
admin.site.register(Cadre)
admin.site.register(OTP)
