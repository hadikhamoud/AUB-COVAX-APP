"""AUBCOVAX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from COVAX import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),
    path('adminclick', views.adminclick_view),
    path('patientclick', views.patientclick_view),


    #path('adminsignup', views.adminsignup_view),
    path('patientsignup', views.patientsignup_view),
    path('viewpatientdosehistory', views.PatientDoseHistory_view),
    path('searchpatients', views.searchpatients_view,name='searchpatients'),
    path('viewpatient/<str:id>', views.viewpatient_view,name='viewpatient'),
    path('adminlogin', LoginView.as_view(template_name='COVAX/adminlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='COVAX/patientlogin.html'),name='patientlogin'),
    path('logout', LogoutView.as_view(template_name='COVAX/index.html')),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('patientlist', views.patientlist_view,name='patientlist'),
    path('MedStafflist', views.MedStafflist_view,name='MedStafflist'),
    path('Patientpersonalinfo', views.Patientpersonalinfo_view,name='Patientpersonalinfo'),
    path('Patientdoseinfo', views.Patientdoseinfo_view,name='Patientdoseinfo'),
    path('PatientCertificate', views.PatientCertificate_view,name='PatientCertificate')


]
