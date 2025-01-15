# main/urls.py
from django.urls import path
from .views import *  # ビューをインポート

# app_name を設定して、名前空間を指定します
app_name = 'employee'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # トップページ用のURL
    path('select_member/', MemberSelectionView.as_view(), name='select_member'),  # 会員選択画面
    path('select_medals/<int:member_id>/', MedalSelectView.as_view(), name='select_medals'),  # 勲章選択画面
]