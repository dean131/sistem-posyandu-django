from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Posyandu


# Register your models here.
class PosyanduAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Posyandu._meta.fields]


admin.site.register(Posyandu, PosyanduAdmin)
