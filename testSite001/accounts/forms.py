from django import forms
from django.core.exceptions import ValidationError
from main.models import *
from django.contrib.auth.forms import UserCreationForm

# カスタムフォーム
class EmployeeCreateForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'password1', 'password2', 'division', 'team', 'position']  # 必要な項目だけを表示

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # パスワードが一致するか確認
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        
        return cleaned_data
