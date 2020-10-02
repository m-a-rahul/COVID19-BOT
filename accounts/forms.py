from .models import Hospitalprofile,Testingprofile,Symptoms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError,EmailField,ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class HospitalCreateForm(UserCreationForm):
    email = EmailField(required=True)
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError(u'This Email Address already holds an account.')
        return email

class TestingCreateForm(UserCreationForm):
    email = EmailField(required=True)
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError(u'This Email Address already holds an account.')
        return email

class HospitalprofileForm(ModelForm):
    class Meta:
        fields =("door_no","street","city","state","contact_no","pin_code","total_beds","occupied_beds","available_beds")
        model = Hospitalprofile

class TestingprofileForm(ModelForm):
    class Meta:
        fields =("door_no","street","city","state","address","contact_no","pin_code","availablity")
        model = Testingprofile
