from django import forms
from django.core.exceptions import ValidationError
from main.models import Member, Medal

class MedalSelectionForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.filter(is_active=True), required=True, label="会員")
    medals = forms.ModelMultipleChoiceField(
        queryset=Medal.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False, 
        label="登録する勲章"
    )
    expiration_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="有効期限")

    def clean_medals(self):
        medals = self.cleaned_data['medals']
        if len(medals) > 5:
            raise ValidationError('最大5つまで選択できます。')
        return medals
