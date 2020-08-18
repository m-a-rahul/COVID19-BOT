from django.contrib import admin
from .models import Hospitalprofile,Testingprofile,Booking

# Register your models here.
admin.site.register(Hospitalprofile)
admin.site.register(Testingprofile)
admin.site.register(Booking)
