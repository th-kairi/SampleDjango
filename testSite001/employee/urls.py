# main/urls.py
from django.urls import path
from .views import IndexView  # クラスベースのビューをインポート

# app_name を設定して、名前空間を指定します
app_name = 'employee'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # トップページ用のURL
]