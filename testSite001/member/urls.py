# main/urls.py
from django.urls import path
from .views import *

# app_name を設定して、名前空間を指定します
app_name = 'member'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # トップページ用のURL
    path('add_points/', AddPointsView.as_view(), name='add_points'),
    path('confirm_add_points/', ConfirmAddPointsView.as_view(), name='confirm_add_points'), # ポイント追加画面
    
# ====================================================================================================
# ===== フリマアプリ
# ====================================================================================================
    path('products/', ProductListView.as_view(), name='product_list'),  # 商品検索画面
    path('products/register/', ProductCreateView.as_view(), name='product_create'),  # 商品登録画面
    path('<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),  # 商品詳細画面
    path('<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),  # 商品編集画面
    path('<int:product_id>/purchase/', ProductPurchaseView.as_view(), name='product_purchase'), # 商品購入画面
    path('cart/confirmation/', CartConfirmationView.as_view(), name='cart_confirmation'), # カート画面


# ====================================================================================================
# ===== スケジュールアプリ
# ====================================================================================================
    
    path('user-schedule-list/', UserScheduleListView.as_view(), name='user_schedule_list'),
    path('add/<str:day>/', EventSelectView.as_view(), name='user_schedule_add'),
    path('schedule/<int:schedule_id>/<int:event_id>/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/<int:id>/delete/', ScheduleDeleteView.as_view(), name='schedule_delete'),  # 削除処理




]