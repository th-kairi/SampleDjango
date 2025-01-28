# main/urls.py
from django.urls import path
from .views import *

# app_name を設定して、名前空間を指定します
app_name = 'member'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # トップページ用のURL
    path('add_points/', AddPointsView.as_view(), name='add_points'),
    path('confirm_add_points/', ConfirmAddPointsView.as_view(), name='confirm_add_points'), # ポイント追加画面
    path('products/', ProductListView.as_view(), name='product_list'),  # 商品検索画面
    path('products/register/', ProductRegisterView.as_view(), name='register_product'),  # 商品登録画面
]