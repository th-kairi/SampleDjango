from django import forms
from main.models import Employee

class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'password', 'division', 'team', 'position', 'zip_code', 'address']

    # パスワードの確認
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="パスワード確認")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("パスワードが一致しません")
        return cleaned_data
