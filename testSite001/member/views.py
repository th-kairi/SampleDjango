from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages
from main.models import *
from django.utils.functional import SimpleLazyObject


class IndexView(TemplateView):
    template_name = 'member/index.html'  # 使用するテンプレートファイル

class AddPointsView(View):
    def get(self, request):
        # ポイント候補値
        point_values = [1000, 2000, 3000, 5000, 10000, 15000, 20000, 30000]

        # ログインユーザーが `Member` モデルかを確認
        if not hasattr(request.user, 'member'):
            # 異なる場合はエラーメッセージを設定してリダイレクト
            messages.error(request, "このページにアクセスする権限がありません。")
            return redirect('member:index')  # リダイレクト先を適切に設定

        # `Wallet` を取得または作成
        wallet, created = Wallet.objects.get_or_create(member=request.user.member)

        # ユーザーのウォレット情報をテンプレートに渡す
        return render(request, 'member/add_points.html', {'wallet': wallet, 'point_values': point_values})

    def post(self, request):
        # フォームから入力されたポイント数を取得
        points_to_add = request.POST.get('points', 0)

        try:
            # ポイントが正の整数であるか確認
            points_to_add = int(points_to_add)
            if points_to_add <= 0:
                raise ValueError

        except (ValueError, TypeError):
            # 無効なポイント入力があった場合のエラーメッセージ
            messages.error(request, "正しいポイントを入力してください。")
            return redirect('member:add_points')  # 入力画面に戻る

        # セッションにポイントを保存し、確認画面へリダイレクト
        request.session['points_to_add'] = points_to_add
        return redirect('member:confirm_add_points')


class ConfirmAddPointsView(View):
    def get(self, request):
        points_to_add = request.session.get('points_to_add')
        if not points_to_add:
            messages.error(request, "追加するポイントが正しく指定されていません。")
            return redirect('member:add_points')  # 入力画面に戻る
        return render(request, 'member/confirm_add_points.html', {'points_to_add': points_to_add})

    def post(self, request):
        # セッションからポイント数を取得
        points_to_add = request.session.pop('points_to_add', None)
        if not points_to_add:
            messages.error(request, "セッションが切れました。もう一度操作してください。")
            return redirect('member:add_points')

        # ユーザーのウォレットにポイントを追加
        wallet = Wallet.objects.get(member=request.user)
        wallet.balance += points_to_add
        wallet.save()

        messages.success(request, f"{points_to_add}ポイントを追加しました。")
        return redirect('member:add_points')
