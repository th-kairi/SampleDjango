# main/views.py
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        # ユーザーがログインしているかを確認
        if user.is_authenticated:
            # Employeeモデルに関連付けられている場合
            if hasattr(user, 'employee'):
                return redirect(reverse_lazy('employee:index'))  # 従業員用アプリのIndexにリダイレクト

            # Memberモデルに関連付けられている場合
            elif hasattr(user, 'member'):
                return redirect(reverse_lazy('member:index'))  # 会員用アプリのIndexにリダイレクト

        # ログインしていない場合やその他のケースは、メインアプリのIndexにリダイレクト
        return super().get(request, *args, **kwargs)