# テンプレート描画とリダイレクトに使用
from django.shortcuts import render, redirect
from django.urls import reverse
# クラスベースビューを作成するための基底クラス
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# 入力処理を作成する際に使うフォーム
from django.forms import *
# モデルインポート
from main.models import *
from .forms import *

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
    
# 商品登録用のビュー
class ProductCreateView(LoginRequiredMixin, View):
    """
    商品登録を行うビュー。
    ユーザーがログインしている場合のみアクセス可能。
    """
    def get(self, request):
        """
        GETリクエストを処理するメソッド。
        フォームを表示する。
        """
        form = ProductForm()  # 新しいフォームを作成
        return render(request, 'products/product_create.html', {'product_form': form})

    def post(self, request):
        """
        POSTリクエストを処理するメソッド。
        商品の登録を行う。
        """
        form = ProductForm(request.POST)  # POSTデータを使用してフォームを作成
        if form.is_valid():  # フォームが有効である場合
            product = form.save(commit=False)  # フォームのデータを保存する前に一時保存
            product.seller = request.user.member  # ログインユーザーを商品出品者として設定
            product.save()  # 商品情報を保存
            self._handle_images(request, product)  # 画像を処理
            return redirect(reverse('member:product_list'))  # 商品リストページにリダイレクト
        else:
            return render(request, 'products/product_create.html', {'product_form': form})

    def _handle_images(self, request, product):
        """
        画像を処理する内部メソッド。
        画像を保存する。
        """
        if 'images' in request.FILES:  # 'images' キーがリクエストに存在するか確認
            images = request.FILES.getlist('images')  # リクエストから画像ファイルを取得
            for image in images:  # 各画像について処理を実行
                ProductImage.objects.create(product=product, image=image)  # 画像を保存

# 商品詳細ビュー
class ProductDetailView(View):
    """
    商品詳細ページビュー。
    ログインユーザーが出品者なら編集画面へ、そうでなければ購入画面へ遷移。
    """
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)  # 商品を取得

        # ログインユーザーが出品者の場合
        if request.user.is_authenticated and product.seller == request.user:
            return redirect(reverse('member:product_edit', args=[product.id]))

        # ログインユーザーが出品者でない場合（購入画面へ）
        return redirect(reverse('member:product_purchase', args=[product.id]))
    
# 商品編集ビュー
class ProductEditView(LoginRequiredMixin, UpdateView):
    """
    商品編集ページビュー。
    ログインユーザーが出品者の場合のみアクセス可能。
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/product_edit.html'  # 作成画面と同じテンプレートを使用

    def get_queryset(self):
        """
        ログインユーザーが出品者である商品を取得。
        """
        return Product.objects.filter(seller=self.request.user.member)

    def get_object(self, queryset=None):
        """
        編集対象の商品を取得。
        """
        product = Product.objects.get(id=self.kwargs['pk'])
        return product

    def get_success_url(self):
        """
        編集成功後のリダイレクト先。
        """
        return reverse('member:product_detail', args=[self.object.id])

# 商品購入ビュー
class ProductPurchaseView(LoginRequiredMixin, View):
    """
    購入画面のビュー。
    """
    def get(self, request, product_id):
        # 選択された商品を取得
        product = Product.objects.get(id=product_id)

        # 同じ出品者の他の商品を取得
        other_products = Product.objects.filter(seller=product.seller).exclude(id=product_id)

        return render(request, 'products/product_purchase.html', {
            'product': product,
            'other_products': other_products,
        })

    def post(self, request, product_id):
        product = Product.objects.filter(id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # カートに商品を追加
        Cart.objects.create(user=request.user, product=product, quantity=quantity)

        return redirect(reverse('products:cart_confirmation'))
    
class CartConfirmationView(LoginRequiredMixin, View):
    """
    カート確認画面ビュー。
    """
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, 'products/cart_confirmation.html', {
            'cart_items': cart_items,
        })

    def post(self, request):
        # カート内の商品を確定して注文番号を生成
        cart_items = Cart.objects.filter(user=request.user)
        order_number = f"ORD-{int(time.time())}"

        for item in cart_items:
            # 必要に応じてOrderモデルで保存
            item.delete()  # カートから削除

        return render(request, 'products/order_success.html', {
            'order_number': order_number,
        })