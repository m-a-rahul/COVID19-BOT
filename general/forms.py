from django.forms import ModelForm
from accounts.models import Booking,Symptoms,Report

class Bookingform(ModelForm):
    class Meta:
        fields = ("name","address","pin_code","contact_no")
        model = Booking

class Symptomsform(ModelForm):
    class Meta:
        fields = ("temprature","cough","headache")
        model = Symptoms

class Reportform(ModelForm):
    class Meta:
        fields = ("result",)
        model = Report
