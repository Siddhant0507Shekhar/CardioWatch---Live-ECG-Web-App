from django.db import models

# Create your models here.
# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)

class Rand(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    # username = models.ForeignKey('User',on_delete=models.CASCADE)