from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms.widgets import DateInput


class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']



class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']

class PatientExtraForm(forms.ModelForm):
    class Meta:
        model = models.PatientExtra
        fields = ["IDCard","PhoneNumber",'DateOfBirth',"City","Country","MedicalConditions"]
        labels = {
        'DateOfBirth': ('D.O.B'),
        'MedicalConditions': ('Medical Conditions'),
        'PhoneNumber': ('Phone Number'),

        }
        widgets = {
        'DateOfBirth': DateInput(attrs={'type': 'date'}),
        'MedicalConditions':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }
