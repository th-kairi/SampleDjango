# staff/urls.py
from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.staff_list, name='staff_list'),  # スタッフ一覧ページ
    path('add/', views.staff_add, name='staff_add'),  # スタッフ追加ページ
    path('<int:pk>/', views.staff_detail, name='staff_detail'),  # スタッフ詳細ページ
]
