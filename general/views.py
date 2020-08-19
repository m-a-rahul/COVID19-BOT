from django.shortcuts import render
from .forms import Bookingform
from accounts.models import Hospitalprofile,Testingprofile,Booking
from random import randint
# Create your views here.
def booking(request,slug):
    if request.method == 'POST':
        form = Bookingform(data=request.POST)
        if form.is_valid():
            upload_form = form.save(commit=False)
            try:
                book = Hospitalprofile.objects.get(slug=slug)
                booking = book.hospital
            except:
                book = Testingprofile.objects.get(slug=slug)
                booking = book.testing
            integrity=False
            while(integrity==False):
                random_code = randint(1000,9999)
                code = 'U'+str(random_code)
                try:
                    Booking.objects.get(naiveuser_id=code)
                    integrity = False
                except :
                    integrity = True
            upload_form.booking = booking
            upload_form.naiveuser_id = code
            upload_form.save()
    else:
        form = Bookingform()
    return render(request,'general/booking_form.html',{'form':form})
