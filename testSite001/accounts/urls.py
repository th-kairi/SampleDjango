
from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_encryption/',
          views.PasswordEncryptionView.as_view(),
          name='password_encryption'
        ),

        # サインアップ:signup
    # path(
    #     "signup",
    #     # TemplateView.as_view(template_name="accounts/signup.html"),
    #     views.SignUpView.as_view(),
    #     name="signup",
    # ),
]
