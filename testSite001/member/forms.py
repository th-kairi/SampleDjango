from django import forms
from main.models import *


class ProductForm(forms.ModelForm):
    """
    商品登録用のフォームを定義するクラス。
    DjangoのModelFormを継承し、データベースモデルと連携。
    """

    class Meta:
        """
        フォームの設定を定義する内部クラス。
        """
        model = Product  # 使用するモデルを指定（Productモデル）
        fields = ['name', 'price', 'description']  # フォームに表示するモデルのフィールドを指定

        # 各フィールドに適用するウィジェットや属性を設定
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',  # CSSクラスを適用
                'placeholder': '商品名を入力してください',  # プレースホルダー
                'required': 'required',  # 必須フィールド
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',  # CSSクラスを適用
                'placeholder': '金額を入力してください（例: 1000）',  # プレースホルダー
                'required': 'required',  # 必須フィールド
                'step': '0.01',  # 小数点を許容する設定
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',  # CSSクラスを適用
                'placeholder': '商品の説明を入力してください',  # プレースホルダー
                'rows': 4,  # テキストエリアの高さを指定
            }),
        }

    def clean_price(self):
        """
        金額フィールドのバリデーションを行うメソッド。
        """
        price = self.cleaned_data.get('price')  # 入力された金額を取得
        if price <= 0:  # 金額が0以下の場合、エラーを発生
            raise forms.ValidationError('金額は正の数値で入力してください。')  # エラーメッセージを表示
        return price  # 問題がなければ金額を返す

    def clean_name(self):
        """
        商品名フィールドのバリデーションを行うメソッド。
        """
        name = self.cleaned_data.get('name')  # 入力された商品名を取得
        if len(name) < 3:  # 商品名が3文字未満の場合、エラーを発生
            raise forms.ValidationError('商品名は3文字以上で入力してください。')  # エラーメッセージを表示
        return name  # 問題がなければ商品名を返す

# ====================================================================================================
# ===== スケジュールアプリ
# ====================================================================================================

class ScheduleSelectionForm(forms.Form):
    """予定の選択フォーム"""
    selected_schedules = forms.ModelMultipleChoiceField(
        queryset=Schedule.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )