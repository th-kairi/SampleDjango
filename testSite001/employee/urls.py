# main/urls.py
from django.urls import path
from .views import *  # ビューをインポート
from accounts.views import *

# app_name を設定して、名前空間を指定します
app_name = 'employee'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # トップページ用のURL
    # 職員作成ページ
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('bulk_create/', BulkEmployeeCreateView.as_view(), name='bulk_employee_create'),
    path('select_member/', MemberSelectionView.as_view(), name='select_member'),  # 会員選択画面
    path('acquired_medals/<int:member_num>/', AcquiredMedalsView.as_view(), name='acquired_medals'),
    path('select_medals/<int:member_num>/', MedalSelectView.as_view(), name='select_medals'),
    path('select_medals/<int:member_num>/<int:medal_id>/', MedalDetailView.as_view(), name='medal_detail'),

]