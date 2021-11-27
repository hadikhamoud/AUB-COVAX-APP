
from django.db import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime, timedelta, date
from django.core.mail import send_mail
from AUBCOVAX.settings import EMAIL_HOST_USER
from datetime import datetime, timezone
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from mailmerge import MailMerge
from datetime import date
from docx2pdf import convert
import mimetypes
from django.http.response import HttpResponse
from django.http import FileResponse

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'COVAX/index.html')
# Create your views here.

def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'COVAX/patientclick.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'COVAX/adminclick.html')

def patientsignup_view(request):
    #form1 for user and form2 to add enrollment and branch
    form1=forms.PatientUserForm()
    form2=forms.PatientExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.PatientUserForm(request.POST)
        form2=forms.PatientExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            obj = models.Appointment()
            obj.Patient = f2
            obj.Dose = "Dose1 Scheduled"
            obj.Dose_one_date = FindAppointment(obj.Dose_one_date)
            obj.save()
            email_subject = 'COVID-19 Vaccination Appointment'
            email_body = 'Hi '+user.first_name+" "+user.last_name+"\nyour COVID-19 Vaccination appointment is on: \n"+str(obj.Dose_one_date)
            #use EmailMessage class to construct email object
            email = EmailMessage(
            email_subject,
            email_body,
            'noreplyaubcovax@gmail.com',
            [user.email]
            )
            email.send(fail_silently=False)
        return HttpResponseRedirect('patientlogin')
    return render(request,'COVAX/patientsignup.html',context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_MedStaff(user):
    return user.groups.filter(name='MedStaff').exists()
def is_Staff(user):
    if user.groups.filter(name='ADMIN').exists():
        return True
    if user.groups.filter(name='MedStaff').exists():
        return True
    return False


def afterlogin_view(request):
    #if admin show admin after login
    if is_admin(request.user):
        return render(request,'COVAX/adminafterlogin.html')
    if is_MedStaff(request.user):
        return render(request,'COVAX/MedStaffafterlogin.html')
    else:
        response =[]
        li = models.Appointment.objects.filter(Patient__user__id = request.user.id)
        if li[0].Dose == 'Dose2 Confirmed':
            response.append(True)
        return render(request,'COVAX/patientafterlogin.html',{'response':response})


@login_required(login_url='adminlogin')
@user_passes_test(is_MedStaff)
def PatientDoseHistory_view(request):
    li = models.Appointment.objects.all()
    return render(request,'COVAX/viewpatientdosehistory.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_Staff)
def searchpatients_view(request):
    credentials = []
    if is_admin(request.user):
        credentials.append(True)
    if request.method=='POST':
        searched = request.POST['searched']
        print(searched)
        patients = models.Appointment.objects.filter(Patient__PhoneNumber__contains = int(searched))
        return render(request, 'COVAX/searchpatients.html',{'li':patients,"credentials":credentials})

    return render(request, 'COVAX/searchpatients.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_MedStaff)
def viewpatient_view(request,id):
    patient = models.Appointment.objects.filter(id = int(id))
    response =[]

    if request.method=='POST':
        Selected = patient[0]
        if Selected.Dose_two_date==None:

            Selected.Dose_one_date = datetime.now()
            Selected.Dose_two_date = FindSecondDoseAppointment()
            print(FindSecondDoseAppointment())
            print(Selected.Dose_two_date)
            Selected.Dose = "Dose2 Scheduled"

            Selected.save()
            email_subject = 'COVID-19 Vaccination Appointment'
            email_body = 'Hi '+Selected.Patient.user.first_name+" "+Selected.Patient.user.last_name+"\nyour COVID-19 2nd Vaccination appointment is on: \n"+str(Selected.Dose_two_date)

            response.append(True)
            email = EmailMessage(
            email_subject,
            email_body,
            'noreplyaubcovax@gmail.com',
            [Selected.Patient.user.email])
            email.send(fail_silently=False)
            response.append(True)
        else:
            Selected.Dose_two_date = datetime.now()
            Selected.Dose = "Dose2 Confirmed"
            Selected.save()
            email_subject = 'COVID-19 Vaccination Certificate'
            path = CreateCertificate(Selected)
            email_body = 'Hi '+Selected.Patient.user.first_name+" "+Selected.Patient.user.last_name+"\nPlease Find your COVID-19 Vaccine Certificate Attached in this email \n"
            email = EmailMessage(
            email_subject,
            email_body,
            'noreplyaubcovax@gmail.com',
            [Selected.Patient.user.email])
            email.attach_file(path)
            email.send(fail_silently=False)



        return render(request, 'COVAX/DoseConfirmed.html',{'response':response})

    return render(request, 'COVAX/viewpatient.html',{'li':patient})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def patientlist_view(request):
    patient = models.Appointment.objects.all()
    return render(request,'COVAX/patientlist.html',{'li':patient})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def MedStafflist_view(request):
    MD = models.User.objects.filter(groups__name="MedStaff")

    return render(request,'COVAX/MedStafflist.html',{'li':MD})


@login_required(login_url='patientlogin')
def Patientpersonalinfo_view(request):
    li = models.PatientExtra.objects.filter(user__id = request.user.id)

    return render(request,'COVAX/Patientpersonalinfo.html',{'li':li})



@login_required(login_url='patientlogin')
def Patientdoseinfo_view(request):
    li = models.Appointment.objects.filter(Patient__user__id = request.user.id)
    li = li[0]
    print(li)

    return render(request,'COVAX/Patientdoseinfo.html',{'li':li})


@login_required(login_url='patientlogin')
def PatientCertificate_view(request):
    li = models.Appointment.objects.filter(Patient__user__id = request.user.id)
    filename = str(li[0].Patient.IDCard)+'.pdf'
    template = ".\static\Certificates\\"
    filepath = template + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
#    return FileResponse(path, content_type='application/pdf')






def FindAppointment(AppointmentDate):
    StartDate = AppointmentDate

    print(StartDate)
    while True:
        temp = models.Appointment.objects.filter(Dose_one_date=StartDate)
        temp2 = models.Appointment.objects.filter(Dose_two_date=StartDate)
        if temp.exists():
            StartDate+= timedelta(minutes=30)
        elif temp2.exists():
            StartDate+= timedelta(minutes=30)
        else:
            return StartDate
        if StartDate.hour == 6:
            nextday = StartDate + timedelta(days=1)
            print(nextday)
            StartDate = datetime(nextday.year,nextday.month,nextday.day,8)


def FindSecondDoseAppointment():
    StartDate = datetime.now() + timedelta(weeks = 3)
    StartDate = datetime(StartDate.year,StartDate.month,StartDate.day,8)
    while True:
        temp = models.Appointment.objects.filter(Dose_one_date=StartDate)
        temp2 = models.Appointment.objects.filter(Dose_two_date=StartDate)
        if temp.exists():
            StartDate+= timedelta(minutes=30)
        elif temp2.exists():
            StartDate+= timedelta(minutes=30)
        else:
            return StartDate
        if StartDate.hour == 6:
            nextday = StartDate + timedelta(days=1)
            print(nextday)
            StartDate = datetime(nextday.year,nextday.month,nextday.day,8)

def CreateCertificate(ib):
    template = ".\static\Certificates"
    document = MailMerge(template+'\Covid-19 vaccination card word.docx')
    print(document.get_merge_fields())

    document.merge(
        Full = str(ib.Patient.user.first_name)+" "+str(ib.Patient.user.last_name),
        DateOfBirth = ib.Patient.DateOfBirth.strftime("%Y-%m-%d"),
        Dose1=ib.Dose_one_date.strftime("%Y-%m-%d %H:%M"),
        IDCard = str(ib.Patient.IDCard),
        Phone = str(ib.Patient.PhoneNumber),
        City = ib.Patient.City,
        Country = ib.Patient.Country,
        Dose2 = ib.Dose_two_date.strftime("%Y-%m-%d %H:%M"))
    document.write(template+str(ib.Patient.IDCard)+'.docx')
    convert(template+str(ib.Patient.IDCard)+'.docx')
    return template+str(ib.Patient.IDCard)+'.pdf'
