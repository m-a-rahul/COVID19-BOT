from django.shortcuts import render
from .forms import HospitalCreateForm,HospitalprofileForm,TestingCreateForm,TestingprofileForm
# Create your views here.
def Hospitalsignup(request):
    if request.method == 'POST':
        hospital_form = HospitalCreateForm(data=request.POST)
        hospital_profile_form = HospitalprofileForm(data=request.POST)
        if hospital_form.is_valid() and hospital_profile_form.is_valid():
            info_form = hospital_form.save(commit=False)
            details_form = hospital_profile_form.save(commit=False)
            details_form.name = info_form.username
            info_form.username = 'HOS'+ str(info_form.id)
            details_form.hospital = info_form
            info_form.save()
            details_form.save()
    else :
        hospital_form = HospitalCreateForm()
        hospital_profile_form = HospitalprofileForm()
    return render(request,'accounts/signup.html',{'hospital_form':hospital_form,
                                                  'hospital_profile_form':hospital_profile_form})
