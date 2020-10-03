from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.contrib.auth.models import User

class Hospitalprofile(models.Model):
    slug = models.SlugField(unique=True,null=True)
    hospital = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=1000)
    door_no = models.CharField(max_length=10)
    street = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    pin_code = models.CharField(max_length=6,validators=[MinLengthValidator(6)])
    contact_no = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    total_beds = models.PositiveSmallIntegerField()
    occupied_beds = models.PositiveSmallIntegerField()
    available_beds = models.PositiveSmallIntegerField()
    merchant_id = models.CharField(max_length=255,null=True,blank=True)
    merchant_key = models.CharField(max_length=255,null=True,blank=True)

    def save(self, *args, **kwargs):
      self.address=self.door_no+", "+self.street+", "+self.city+", "+self.state+", "+self.pin_code
      super(Hospitalprofile, self).save(*args, **kwargs)

class Testingprofile(models.Model):
    slug = models.SlugField(unique=True,null=True)
    testing = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=1000)
    door_no = models.CharField(max_length=10)
    street = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    pin_code = models.CharField(max_length=6,validators=[MinLengthValidator(6)])
    contact_no = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    availablity = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
      self.address=self.door_no+", "+self.street+", "+self.city+", "+self.state+", "+self.pin_code
      super(Testingprofile, self).save(*args, **kwargs)

class Booking(models.Model):
    naiveuser_id = models.CharField(max_length=10)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=1000)
    pin_code = models.CharField(max_length=6,validators=[MinLengthValidator(6)])
    contact_no = models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    booking = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255,null=True,blank=True)
    payment = models.BooleanField(default=False)

class Symptoms(models.Model):
    naiveuser_id = models.ForeignKey(Booking,on_delete=models.CASCADE)
    temprature = models.BooleanField()
    cough = models.BooleanField()
    headache = models.BooleanField()

class Report(models.Model):
    naiveuser_id = models.OneToOneField(Booking,on_delete=models.CASCADE)
    result_choices = (('Positive','Positive'),('Negative','Negative'))
    result = models.CharField(choices=result_choices,max_length=20)
