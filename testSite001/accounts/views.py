# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
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

# 職員アカウント作成
class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = 'accounts/employee_create.html'
    success_url = reverse_lazy('employee:index')  # 職員一覧ページにリダイレクトする例

    def form_valid(self, form):
        # パスワードを暗号化して保存する処理（もし必要な場合）
        employee = form.save(commit=False)
        employee.set_password(form.cleaned_data['password1'])
        employee.save()
        messages.success(self.request, '職員が作成されました。')
        return redirect(self.success_url)

    def form_invalid(self, form):
        # エラーメッセージが表示される
        messages.error(self.request, '職員作成に失敗しました。')
        # フォームが無効な場合、エラーメッセージを表示
        return self.render_to_response(self.get_context_data(form=form))
    
# 職員一括登録
class BulkEmployeeCreateView(View):
    # GETリクエストを処理するメソッド
    def get(self, request):
        # フォームセットのインスタンスを作成（フォームセットは複数のフォームをまとめて処理できるもの）
        formset = BulkEmployeeFormSet()

        # フォームセットをテンプレートに渡して、ユーザーに表示する
        return render(request, 'accounts/bulk_employee_create.html', {'formset': formset})

    # POSTリクエストを処理するメソッド
    def post(self, request):
        
        # TOTAL_FORMSを動的に設定
        num_entries = len(request.POST.getlist('name'))  # nameのリストから職員数を取得
        request.POST = request.POST.copy()  # POSTデータをコピーして変更可能にする
        print("request.POST.get('form-TOTAL_FORMS'):", request.POST.get('form-TOTAL_FORMS'))
        request.POST['form-TOTAL_FORMS'] = request.POST.get('form-TOTAL_FORMS')

        # POSTデータを使ってフォームセットを再生成
        formset = BulkEmployeeFormSet(request.POST)# フォームセットの各フォームのデータを出力
        # デバッグ用: POSTされたデータを確認
        print('==========================================================================')
        print('BulkEmployeeCreateView:post')  # このメソッドが呼ばれたことを確認するためのログ
        print('request.POST:', request.POST)  # POSTデータ（フォームに入力されたデータ）の内容を表示
        print('-------------------------------------')
        print("request.POST['form-TOTAL_FORMS']:", request.POST['form-TOTAL_FORMS'])
        print("request.POST['form-INITIAL_FORMS']:",request.POST['form-INITIAL_FORMS'])
        # print(f"TOTAL_FORMS in formset: {formset.total_form_count}")
        print('-------------------------------------')

        # フォームセットが正常にバリデーションを通過しているか確認
        print('formset:', formset)  # フォームセットが適切に作成されているかを確認するログ

        # フォームセットが有効かどうかを確認
        if formset.is_valid():
            print('formset.is_valid()')  # バリデーションが成功した場合のログ

            # 有効なフォームがある場合、各フォームのデータを保存
            for form in formset:
                # 各フォームのデータを保存
                form.save() # 保存処理
                print(f"Saving form: {form.cleaned_data}")  # 保存するフォームのデータ（クリーニングされたデータ）を表示

            # 成功メッセージをユーザーに通知
            print('職員が一括で作成されました。')
            messages.success(request, '職員が一括で作成されました。')

            # 成功したらリダイレクト（職員一覧ページなどへ遷移）
            return redirect('employee:bulk_employee_create')  # 'employee:index' は職員一覧ページへのURL名

        # フォームセットが無効な場合、エラーメッセージを表示
        print('職員作成に失敗しました。再度入力を確認してください。')
        messages.error(request, '職員作成に失敗しました。再度入力を確認してください。')

        # フォームセットのエラーメッセージをデバッグ用に表示
        print(formset.errors)  # エラー内容をログに出力してデバッグ

        # エラーが発生した場合は、再度フォームを表示（ユーザーが入力を修正できるようにする）
        return render(request, 'accounts/bulk_employee_create.html', {'formset': formset})
