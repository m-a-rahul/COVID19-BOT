from django.shortcuts import render
from .forms import Bookingform,Symptomsform
from accounts.models import Hospitalprofile,Testingprofile,Booking
from random import randint
from django.contrib import messages
# Create your views here.
def Homepage(request):
    current_instance ="Null"
    is_hospital = "Null"
    bookings_under = "No bookings"
    if request.user.is_authenticated and not request.user.is_superuser:
        try:
            current_instance = Hospitalprofile.objects.get(hospital=request.user)
            is_hospital="True"
        except:
            current_instance = Testingprofile.objects.get(testing=request.user)
            is_hospital="False"
        try:
            bookings_under=Booking.objects.filter(booking=request.user)
        except :
            bookings_under = "No bookings"
    hospitals = Hospitalprofile.objects.raw('SELECT * FROM accounts_hospitalprofile')
    testing = Testingprofile.objects.all()
    filteredhospitals = []
    filteredtesting = []
    if request.method == "POST":
        pin = request.POST.get('pin_code')
        pin = int(pin)
        i=1
        j=1
        while(len(filteredhospitals)<5 and i <=10):
            pin1 = pin-i
            pin2 =pin+i
            filteredhospitals = Hospitalprofile.objects.raw('SELECT * FROM accounts_hospitalprofile where pin_code>=%d and pin_code<=%d'%(pin1,pin2))
            i+=1
        while(len(filteredtesting)<5 and j <=10):
            pin1 = pin-j
            pin2 =pin+j
            filteredtesting = Testingprofile.objects.raw('SELECT * FROM accounts_testingprofile where pin_code>=%d and pin_code<=%d'%(pin1,pin2))
            j+=1
        if len(filteredhospitals) is 0:
            messages.warning(request,'There are no hospitals nearby to this pincode')
        if len(filteredtesting) is 0:
            messages.warning(request,'There are no testing facilities nearby to this pincode')
    if bookings_under != "No bookings":
        if bookings_under.count() is 0:
            bookings_under = "No bookings"
    return render(request,'index.html',{'hospitals':hospitals,
                                         'testing':testing,
                                         'filteredhospitals':filteredhospitals,
                                         'filteredtesting':filteredtesting,
                                         'is_hospital':is_hospital,
                                         'bookings_under':bookings_under,
                                         'current_instance':current_instance})

def booking(request,slug):
    if request.method == 'POST':
        form = Bookingform(data=request.POST)
        symptoms = Symptomsform(data=request.POST)
        if form.is_valid() and symptoms.is_valid():
            upload_form = form.save(commit=False)
            symptoms_form = symptoms.save(commit=False)
            try:
                book = Hospitalprofile.objects.get(slug=slug)
                #raw('SELECT * FROM accounts_hospitalprofile where slug = %s' %slug)
                booking = book.hospital
            except:
                book = Testingprofile.objects.get(slug=slug)
                #raw('SELECT * FROM accounts_testingprofile where slug = %s' %slug)
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
            symptoms_form.naiveuser_id = upload_form
            upload_form.naiveuser_id = code
            upload_form.save()
            symptoms_form.save()
    else:
        form = Bookingform()
        symptoms = Symptomsform()
    return render(request,'general/booking_form.html',{'form':form,'symptoms':symptoms})
