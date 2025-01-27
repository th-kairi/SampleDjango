from django import forms
from main.models import *
from django.forms import formset_factory

# カスタムフォーム
class EmployeeCreateForm(forms.ModelForm):
    # パスワードフィールドを通常のCharFieldに変更
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Employee
        fields = ['name', 'email', 'password1', 'division', 'team', 'position']  # 必要な項目だけを表示

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        
        return cleaned_data
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # ここではパスワードのバリデーションを行わない
        return password

# 職員一括登録
class BulkEmployeeCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    division = forms.CharField(max_length=100, required=False)  # 部署の自由入力
    team = forms.CharField(max_length=100, required=False)  # 部門の自由入力

    
    # 入力フォームの属性の設定
    # bootstrap を利用する為Classの設定を使ってCSSを適応する
    def __init__(self, *args, **kwrags):
        super().__init__(*args, **kwrags)
        # class の設定（htmlから転記）
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["division"].widget.attrs["class"] = "form-control"
        self.fields["team"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Employee
        fields = ['name', 'email', 'division', 'team']

    def clean_division(self):
        division = self.cleaned_data.get('division')
        # 部門が空でないことを確認
        if division and not position.objects.filter(name=division, type='部署').exists():
            raise forms.ValidationError("指定された部門は存在しません。")
        return division

    def clean_team(self):
        team = self.cleaned_data.get('team')
        # 部署が空でないことを確認
        if team and not position.objects.filter(name=team, type='課').exists():
            raise forms.ValidationError("指定された部署は存在しません。")
        return team

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.set_password(employee.name)  # 名前をパスワードとして設定
        if commit:
            employee.save()
        return employee

# フォームセットを作成
BulkEmployeeFormSet = formset_factory(BulkEmployeeCreateForm, extra=1)  # 初期フォームを1つ表示
