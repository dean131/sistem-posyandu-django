from django.contrib import admin
from .models import PosyanduActivity


# Register your models here.
class PosyanduActivityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PosyanduActivity._meta.fields]


admin.site.register(PosyanduActivity, PosyanduActivityAdmin)
