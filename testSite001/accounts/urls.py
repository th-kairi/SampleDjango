
from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

# app_name を設定して、名前空間を指定します
app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_encryption/',
          views.PasswordEncryptionView.as_view(),
          name='password_encryption'
        ),
]
