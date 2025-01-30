# staff/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # スタッフIndex
    path('', views.IndexView.as_view(), name='index'),  
    # スタッフ一覧ページ
    path('staff_list/', views.StaffListView.as_view(), name='staff_list'),  
    # スタッフ追加ページ
    path('add/', views.StaffCreateView.as_view(), name='staff_add'),
    # スタッフ詳細ページ
    path('<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'), 
    # シフト一覧ページ
    path('shift-schedule-list/', views.ShiftScheduleListView.as_view(), name='shift_schedule_list'),
    # シフト一覧ページ
    path('shift-schedule-list/<int:staff_id>/', views.ShiftScheduleListView.as_view(), name='shift_schedule_list_for_staff'),
    # スタッフシフト詳細ページ
    path('shift-schedule-detail/<int:pk>/', views.StaffShiftDetailView.as_view(), name='staff_shift_detail'),
    # シフト確認画面
    path('shift-schedule/<int:pk>/', views.ShiftScheduleView.as_view(), name='shift_schedule'),
    # シフト確認画面
    path('staff_shift_schedule/', views.StaffListView.as_view(), name='staff_shift_schedule'),


# ====================================================================================================
# ===== スケジュールアプリ
# ====================================================================================================    

    # 予定一覧を表示するページのURL
    path('schedule-search/', views.ScheduleListView.as_view(), name='schedule_list'),
    # 予定を新規作成するページのURL
    path('new/', views.ScheduleCreateView.as_view(), name='schedule_create'),
    # 予定を編集するページのURL（pkは予定のID）
    path('<int:pk>/edit/', views.ScheduleUpdateView.as_view(), name='schedule_edit'),
    # 予定を削除するページのURL（確認画面を表示）
    path('<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule_delete'),
]


# メディアファイルのURLを設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)