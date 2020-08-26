from django.shortcuts import render
from .forms import Bookingform
from accounts.models import Hospitalprofile,Testingprofile,Booking
from random import randint
from accounts.models import Hospitalprofile,Testingprofile
# Create your views here.
def Homepage(request):
    hospitals = Hospitalprofile.objects.raw('SELECT * FROM accounts_hospitalprofile')
    testing = Testingprofile.objects.all()
    filteredhospitals = []
    if request.method == "POST":
        pin = request.POST.get('pin_code')
        pin = int(pin)
        i=1
        while(len(filteredhospitals)<5 and i <=10):
            pin1 = pin-i
            pin2 =pin+i
            filteredhospitals = Hospitalprofile.objects.raw('SELECT * FROM accounts_hospitalprofile where pin_code>=%d and pin_code<=%d'%(pin1,pin2))
            i+=1
    return render(request,'index.html',{'hospitals':hospitals,
                                         'testing':testing,
                                         'filteredhospitals':filteredhospitals})

def booking(request,slug):
    if request.method == 'POST':
        form = Bookingform(data=request.POST)
        if form.is_valid():
            upload_form = form.save(commit=False)
            try:
                book = Hospitalprofile.objects.raw('SELECT * FROM accounts_hospitalprofile WHERE slug = slug')
                booking = book.hospital
            except:
                book = Testingprofile.objects.raw('SELECT * FROM accounts_testingprofile WHERE slug = slug')
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
