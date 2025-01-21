# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .forms import *

# CustomUserモデルを取得
User = get_user_model()

# ログインビュー
class LoginView(LoginView):
    template_name = 'accounts/login.html'  # ログインページのテンプレート

    def get_success_url(self):
        # ログインしたユーザーがどのモデルに属しているかを確認
        user = self.request.user
        
        # Employeeモデルの場合
        if hasattr(user, 'employee'):  # Employeeに関連付けられているかを確認
            return reverse_lazy('employee:index') # 従業員用アプリのIndexにリダイレクト
        
        # Memberモデルの場合
        elif hasattr(user, 'member'):  # Memberに関連付けられているかを確認
            return reverse_lazy('member:index') # 会員用アプリのIndexにリダイレクト
        
        # それ以外（デフォルト）は管理者ページなど
        return reverse_lazy('main:index')  # mainアプリのIndexにリダイレクト

# ログアウトビュー
class LogoutView(LogoutView):
    next_page = '/'  # ログアウト後のリダイレクト先

class PasswordEncryptionView(View):
    # スタッフのみアクセス可能
    def dispatch(self, request, *args, **kwargs):
        # request.userがスタッフ権限を持っていない場合、リダイレクト
        if not request.user.is_staff:
            return redirect('accounts:login')  # ログインページにリダイレクト
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # 'is_password_encrypted' フィールドで暗号化されていないユーザーをフィルタリング
        users = User.objects.filter(is_password_encrypted=False)
        
        # 現在のログインユーザー情報
        current_user = request.user  # 正しい方法: request.user を使う

        # ここでusersをテンプレートに渡す
        return render(request, 'accounts/password_encryption.html', {'users': users, 'current_user': current_user})

    def post(self, request):
        # 'is_password_encrypted' フィールドで暗号化されていないユーザーをフィルタリング
        users = User.objects.filter(is_password_encrypted=False)
        
        # パスワードを暗号化
        for user in users:
            user.set_password(user.password)  # set_passwordで暗号化
            user.is_password_encrypted = True  # フィールド名を修正
            user.save()
        
        messages.success(request, "選択されたユーザーのパスワードを暗号化しました。")
        return redirect('accounts:password_encryption')

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = 'accounts/employee_create.html'
    success_url = reverse_lazy('employee:employee_list')  # 職員一覧ページにリダイレクトする例

    def form_valid(self, form):
        # パスワードを暗号化して保存する処理（もし必要な場合）
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, '職員が作成されました。')
        return redirect(self.success_url)

    def form_invalid(self, form):
        # エラーメッセージが表示される
        messages.error(self.request, '職員作成に失敗しました。')
        return self.render_to_response({'form': form})