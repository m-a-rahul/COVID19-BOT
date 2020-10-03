from django.shortcuts import render
from .forms import Bookingform,Symptomsform,Reportform
from accounts.models import Hospitalprofile,Testingprofile,Booking
from random import randint
from django.contrib import messages
from twilio.rest import Client
from BOT import secrets
from paytm import checksum
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
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
                amount = 1500
            except:
                book = Testingprofile.objects.get(slug=slug)
                #raw('SELECT * FROM accounts_testingprofile where slug = %s' %slug)
                booking = book.testing
                amount = 300
            integrity=False
            while(integrity==False):
                random_code = randint(1000,9999)
                code = 'U'+str(random_code)
                try:
                    Booking.objects.get(naiveuser_id=code)
                    integrity = False
                except :
                    integrity = True
            customer_name = upload_form.name
            upload_form.booking = booking
            symptoms_form.naiveuser_id = upload_form
            upload_form.naiveuser_id = code
            print(upload_form.payment)
            upload_form.save()
            symptoms_form.save()
            #Paytm
            order_name = slugify(upload_form.name)
            order_date = slugify(datetime.datetime.now())
            order_id = slugify(order_name+order_date)
            MERCHANT_KEY = secrets.MERCHANT_KEY
            if upload_form.payment:
                param_dict = {
                        'MID': secrets.MERCHANT_ID,
                        'ORDER_ID': str(order_id),
                        'TXN_AMOUNT': str(amount),
                        'CUST_ID': customer_name,
                        'INDUSTRY_TYPE_ID': 'Retail',
                        'WEBSITE': 'WEBSTAGING',
                        'CHANNEL_ID': 'WEB',
                        'CALLBACK_URL':'http://127.0.0.1:8000/general/paytm/',

                        }
                param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
                return render(request, 'general/paytm.html',{'param_dict':param_dict})
    else:
        form = Bookingform()
        symptoms = Symptomsform()
    return render(request,'general/booking_form.html',{'form':form,'symptoms':symptoms})


@csrf_exempt
def paytm_handle(request):
    form = request.POST
    response_dict = {}
    MERCHANT_KEY = secrets.MERCHANT_KEY
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            Checksum = form[i]
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, Checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            messages.success(request, 'Your booking has been registered')
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'general/paymentstatus.html', {'response': response_dict})


def Report(request,slug):
    booking = Booking.objects.get(naiveuser_id=slug)
    account_sid = secrets.account_sid
    auth_token  = secrets.auth_token
    client = Client(account_sid, auth_token)
    if request.method == 'POST':
        form=Reportform(data=request.POST)
        if form.is_valid():
            upload_form =form.save(commit=False)
            upload_form.naiveuser_id = booking
            if upload_form.result == 'Postive':
                message = client.messages.create(
                            to="+919150114577",
                            from_="+19285890874",
                            body="You have been tested positive")
            else:
                message = client.messages.create(
                            to="+919150114577",
                            from_="+19285890874",
                            body="You have been tested negative")
            upload_form.save()
    else:
        form=Reportform()
    return render(request,'general/report_form.html',{'form':form})
