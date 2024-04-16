from django.contrib import admin


from base.models import (
    Village,
    Child,
    Posyandu,
)


class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'current_age')

admin.site.register(Village) 
admin.site.register(Child, ChildAdmin)   
admin.site.register(Posyandu)
