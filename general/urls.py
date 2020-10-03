from django.urls import path
from general import views

app_name = 'general'

urlpatterns = [
    path('booking/<slug>',views.booking,name='booking'),
    path('result/<slug>',views.Report,name='result'),
    path('paytm/',views.paytm_handle,name="handlerequest"),
]
