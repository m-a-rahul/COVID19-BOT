from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.contrib.auth.models import User
# Create your models here.
class Hospitalprofile(models.Model):
    hospital = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=1000)
    pin_code = models.CharField(max_length=6,validators=[MinLengthValidator(6)])
    contact_no = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    total_beds = models.PositiveSmallIntegerField()
    occupied_beds = models.PositiveSmallIntegerField()
    available_beds = models.PositiveSmallIntegerField()

class Testingprofile(models.Model):
    testing = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=1000)
    pin_code = models.CharField(max_length=6,validators=[MinLengthValidator(6)])
    contact_no = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    availablity = models.PositiveSmallIntegerField()
