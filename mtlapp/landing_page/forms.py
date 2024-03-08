from django.forms import ModelForm
from django import forms
from .models import Student
from django.db import models
from django.utils import timezone
import datetime as dt

PHASE_CHOICES =(("0", "0"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"))

class ScanForm(ModelForm):
    '''
    This class ScanForm is a built in form in django that can take a user input and return it to a view request.
    Forms are consisted of Posts and Gets. Posts hide their data, and Gets display it in the url.
    There are benefits and drawbacks to each, but Posts are more secure.
    You can read more about how to use forms them at: https://docs.djangoproject.com/en/5.0/topics/forms/.
    This form is referenced in the checkinout and checkinoutbad htmls. The views for these htmls read the post data
    (in this case, a CAC UUID scan) and can manipulate it.
    '''
    uuid = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'autofocus': True}))
    
    class Meta:
        model = Student
        fields = ['uuid']


class UpdatePhase(ModelForm):
    '''
    '''
    phase = forms.ChoiceField(choices = PHASE_CHOICES)
    uuid = forms.CharField(max_length=30)

    class Meta:
        model = Student
        fields = ['phase', 'uuid']


class StudentSearch(ModelForm):
    '''
    '''
    Last_Name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'autofocus': True, 'autocomplete': 'off'}))

    class Meta:
        model = Student
        fields = ['Last_Name']

