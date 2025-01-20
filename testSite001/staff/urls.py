# staff/urls.py
from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # スタッフ一覧ページ
    path('', views.StaffListView.as_view(), name='staff_list'),  
    # スタッフ追加ページ
    path('add/', views.StaffCreateView.as_view(), name='staff_add'),
    # スタッフ詳細ページ
    path('<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'), 
    # シフト一覧ページ
    path('shift-schedule-list/', views.ShiftScheduleListView.as_view(), name='shift_schedule_list'),
    # スタッフシフト詳細ページ
    path('shift-schedule-detail/<int:pk>/', views.StaffShiftDetailView.as_view(), name='staff_shift_detail'),
    # シフト確認画面
    path('shift-schedule/<int:pk>/', views.ShiftScheduleView.as_view(), name='shift_schedule'),
    # シフト確認画面
    path('staff_shift_schedule/', views.StaffListView.as_view(), name='staff_shift_schedule'),

    

]
