from django.shortcuts import render
from .forms import Bookingform
from accounts.models import Hospitalprofile,Testingprofile,Booking
from random import randint
from accounts.models import Hospitalprofile,Testingprofile
from django.contrib import messages
# Create your views here.
def Homepage(request):
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
            messages.warning(request,'There are no testing nearby to this pincode')
    return render(request,'index.html',{'hospitals':hospitals,
                                         'testing':testing,
                                         'filteredhospitals':filteredhospitals,
                                         'filteredtesting':filteredtesting})

def booking(request,slug):
    if request.method == 'POST':
        form = Bookingform(data=request.POST)
        if form.is_valid():
            upload_form = form.save(commit=False)
            try:
                book = Hospitalprofile.objects.get(slug=slug)
                #raw('SELECT * FROM accounts_hospitalprofile where slug = %s' %slug)
                print(book)
                booking = book.hospital
            except:
                book = Testingprofile.objects.get(slug=slug)
                #raw('SELECT * FROM accounts_testingprofile where slug = %s' %slug)
                print(book)
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
