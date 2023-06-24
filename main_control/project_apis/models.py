from django.db import models
from django.contrib.auth.models import User

# from django.contrib.gis.db import models
# from .models import Ecg_data
# Create your models here.
class Health_Status(models.Model):
    health = models.IntegerField()
    date = models.DateField()
    timer = models.TimeField()
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)


class Ecg_data(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE)
    ecg_image = models.ImageField()
    date_time = models.DateTimeField()
    heart_beat = models.IntegerField(default=70)
    langitude = models.CharField(default=29.86,max_length=20)
    latitude = models.CharField(default=77.90,max_length=20)
    altitude = models.CharField(default=264.20,max_length=20)
    ecg_arr = models.CharField(default=str([20 for i in range(600)]),max_length=4000)

    class Meta:
        ordering = ['-date_time']
