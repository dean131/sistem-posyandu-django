from django.contrib import admin
from .models import Child


# Register your models here.
class ChildAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Child._meta.fields]


admin.site.register(Child, ChildAdmin)
