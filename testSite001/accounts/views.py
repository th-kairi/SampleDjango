# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib import messages

# CustomUserモデルを取得
User = get_user_model()

# ログインビュー
class LoginView(LoginView):
    template_name = 'accounts/login.html'  # ログインページのテンプレート

# ログアウトビュー
class LogoutView(LogoutView):
    next_page = '/'  # ログアウト後のリダイレクト先

class PasswordEncryptionView(View):
    # スタッフのみアクセス可能
    @user_passes_test(lambda user: user.is_staff)
    def get(self, request):
        # 「暗号化フラグ」がFalseのユーザーのみを取得
        users = User.objects.filter(encrypted=False)
        return render(request, 'accounts/password_encryption.html', {'users': users})

    # スタッフのみアクセス可能
    @user_passes_test(lambda user: user.is_staff)
    def post(self, request):
        # 暗号化フラグがFalseのユーザーのみを取得
        users = User.objects.filter(encrypted=False)
        
        # パスワードを暗号化
        for user in users:
            user.set_password(user.password)  # set_passwordで暗号化
            user.encrypted = True  # 暗号化フラグをTrueに設定
            user.save()
        
        messages.success(request, "選択されたユーザーのパスワードを暗号化しました。")
        return redirect('accounts:password_encryption')
