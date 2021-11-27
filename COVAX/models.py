from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta,timezone


class PatientExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    IDCard = models.IntegerField()
    PhoneNumber = models.IntegerField()
    DateOfBirth = models.DateTimeField()
    City = models.CharField(max_length=40)
    Country = models.CharField(max_length=40)
    MedicalConditions = models.CharField(max_length=400)
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+' ['+str(self.PhoneNumber)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id
    @property
    def getusernum(self):
        return self.PhoneNumber


def getfirstDoseDate():
    now = datetime.today()
    tomorrow = now + timedelta(days = 1)
    DoseDate = datetime(tomorrow.year,tomorrow.month,tomorrow.day,8)
    return DoseDate


class Appointment(models.Model):
    Patient = models.ForeignKey('PatientExtra', on_delete=models.CASCADE,null=True)
    Dose = models.CharField(max_length=40)
    Dose_one_date = models.DateTimeField(default=getfirstDoseDate())
    Dose_two_date = models.DateTimeField(null=True)
    def __str__(self):
        return self.Patient.user.first_name+" "+self.Patient.user.last_name
