from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Village


# Register your models here.
class VillageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Village._meta.fields]


admin.site.register(Village, VillageAdmin)

# Customizing Django Admin
admin.site.site_header = _("Posyandu Admin")
admin.site.site_title = _("Posyandu Admin")
admin.site.index_title = _("Selamat Datang di Admin Posyandu")
