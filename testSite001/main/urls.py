# main/urls.py
from django.urls import path
from .views import IndexView  # クラスベースのビューをインポート

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # トップページ用のURL
]