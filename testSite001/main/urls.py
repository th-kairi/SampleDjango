# main/urls.py
from django.urls import path
from .views import *  # クラスベースのビューをインポート
from django.urls import path

# app_name を設定して、名前空間を指定します
app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # トップページ用のURL
]