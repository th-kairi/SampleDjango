# staff/forms.py
from django import forms
from main.models import *


# ====================================================================================================
# ===== シフトアプリ
# ====================================================================================================

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'division', 'team', 'position', 'hire_date', 'phone_number', 'rank']


# ====================================================================================================
# ===== スケジュールアプリ
# ====================================================================================================


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule  # モデルに対応するフォーム
        fields = ['title', 'image', 'description', 'category', 'importance', 'is_completed']  # 画像フィールドを追加
        labels = {
            'title': '予定タイトル',
            'image': 'イメージ画像',
            'description': '詳細情報',
            'category': 'カテゴリ',
            'importance': '重要度',
            'is_completed': '完了',
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'