from django.shortcuts import render
from .forms import HospitalCreateForm,HospitalprofileForm,TestingCreateForm,TestingprofileForm
from random import randint
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your views here.
def Hospitalsignup(request):
    if request.method == 'POST':
        hospital_form = HospitalCreateForm(data=request.POST)
        hospital_profile_form = HospitalprofileForm(data=request.POST)
        if hospital_form.is_valid() and hospital_profile_form.is_valid():
            info_form = hospital_form.save(commit=False)
            details_form = hospital_profile_form.save(commit=False)
            details_form.name = info_form.username
            integrity=False
            while(integrity==False):
                random_code = randint(1000,9999)
                code = 'HOS'+str(random_code)
                try:
                    User.objects.get(username=code)
                    integrity = False
                except :
                    integrity = True
            if integrity:
                info_form.username = code
                details_form.slug = slugify(code)
                details_form.hospital = info_form
                info_form.save()
                details_form.save()
    else :
        hospital_form = HospitalCreateForm()
        hospital_profile_form = HospitalprofileForm()
    return render(request,'accounts/signup.html',{'form':hospital_form,
                                                  'profile_form':hospital_profile_form})

def Testingsignup(request):
    if request.method == 'POST':
        test_form = TestingCreateForm(data=request.POST)
        test_profile_form = TestingprofileForm(data=request.POST)
        if test_form .is_valid() and test_profile_form.is_valid():
            info_form = test_form.save(commit=False)
            details_form = test_profile_form.save(commit=False)
            details_form.name = info_form.username
            integrity=False
            while(integrity==False):
                random_code = randint(1000,9999)
                code = 'TES'+str(random_code)
                try:
                    User.objects.get(username=code)
                    integrity = False
                except :
                    integrity = True
            info_form.username = code
            details_form.testing = info_form
            details_form.slug = slugify(code)
            info_form.save()
            details_form.save()
    else :
        test_form = TestingCreateForm()
        test_profile_form = TestingprofileForm()
    return render(request,'accounts/signup.html',{'form':test_form,
                                                  'profile_form':test_profile_form})
