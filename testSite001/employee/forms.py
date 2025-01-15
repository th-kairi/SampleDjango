from django import forms
from main.models import *

class MemberSelectionForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.filter(is_active=True), required=True, label="会員")
