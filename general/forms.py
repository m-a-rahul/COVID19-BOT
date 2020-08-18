from django.forms import ModelForm
from accounts.models import Booking

class Bookingform(ModelForm):
    class Meta:
        fields = ("name","address","pin_code","contact_no")
        models = Booking
