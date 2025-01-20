# staff/forms.py
from django import forms
from main.models import *

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'division', 'team', 'position', 'hire_date', 'phone_number', 'rank']
