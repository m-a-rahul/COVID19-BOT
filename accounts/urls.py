from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/hospital',views.Hospitalsignup,name='hsignup'),
    path('signup/testing',views.Testingsignup,name='tsignup')

]
