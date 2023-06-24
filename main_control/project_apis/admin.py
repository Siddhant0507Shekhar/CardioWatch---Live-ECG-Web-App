from django.contrib import admin

# Register your models here.
from .models import Health_Status, Ecg_data

admin.register(Health_Status)
admin.site.register(Health_Status)

admin.register(Ecg_data)
admin.site.register(Ecg_data)