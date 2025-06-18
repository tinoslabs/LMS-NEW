from django.contrib import admin

# Register your models here.
from.models import Guest,Guest_ProfilePermission

admin.site.register(Guest_ProfilePermission) 
admin.site.register(Guest) 