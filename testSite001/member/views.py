from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.contrib import messages
from django.forms import *
from main.models import *


class IndexView(TemplateView):
    template_name = 'member/index.html'  # 使用するテンプレートファイル

# ポイント追加ビュー
class AddPointsView(View):
    def get(self, request):
        # ポイント候補値 画面上に表示される追加候補ボタンの値
        point_values = [1000, 2000, 3000, 5000, 10000, 15000, 20000, 30000]

        # ログインユーザーが `Member` モデルかを確認
        if not hasattr(request.user, 'member'):
            # 異なる場合はエラーメッセージを設定してリダイレクト
            messages.error(request, "このページにアクセスする権限がありません。")
            return redirect('member:index')  # リダイレクト先を適切に設定

        # Walletの存在チェックをして取得または作成
        wallet, created = Wallet.objects.get_or_create(member=request.user.member)

        # ユーザーのWallet情報をテンプレートに渡す
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

# 追加ポイント確認ビュー
class ConfirmAddPointsView(View):
    def get(self, request):
        # セッションから追加ポイントを取得
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
    
# 商品検索ビュー
class ProductListView(ListView):
    model = Product  # 表示対象のモデル
    template_name = 'products/product_list.html'  # 使用するテンプレート
    context_object_name = 'products'  # テンプレート内で使う変数名

    def get_queryset(self):
        """
        検索キーワードに基づいて商品をフィルタリング
        """
        query = self.request.GET.get('q', '')  # クエリパラメータを取得
        queryset = Product.objects.prefetch_related('images')  # 画像を事前取得
        if query:
            return Product.objects.filter(name__icontains=query)  # 部分一致検索
        return Product.objects.all()  # 全件表示

# 商品登録ビュー
class ProductRegisterView(View):
    class ProductForm(ModelForm):
        """
        商品情報フォーム
        """
        class Meta:
            model = Product
            fields = ['name', 'description', 'price']

    def get(self, request):
        product_form = self.ProductForm()
        return render(request, 'products/register_product.html', {
            'product_form': product_form,
        })

    def post(self, request):
        product_form = self.ProductForm(request.POST)

        if product_form.is_valid():
            # 商品データを保存
            product = product_form.save(commit=False)
            try:
                # ログインユーザーが Member モデルであることを確認
                member_instance = Member.objects.get(pk=request.user.pk)
            except Member.DoesNotExist:
                return redirect('member:index')  # エラー処理

            product.seller = member_instance
            product.save()

            # 画像データを保存
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)

            return redirect('member:product_list')
        else:
            print("フォームエラー:", product_form.errors)

        return render(request, 'products/register_product.html', {
            'product_form': product_form,
        })
    


