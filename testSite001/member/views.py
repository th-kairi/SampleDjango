# テンプレート描画とリダイレクトに使用
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
# クラスベースビューを作成するための基底クラス
from django.views.generic import TemplateView, ListView, ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.forms import *
from main.models import *
from .forms import *
import uuid

# ---------------------------------------------------------------------
# トップページビュー
# ---------------------------------------------------------------------
class IndexView(TemplateView):
    template_name = 'member/index.html'  # 使用するテンプレートファイル

# ---------------------------------------------------------------------
# ポイント追加ビュー
# ---------------------------------------------------------------------
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
        # `get_or_create` は、該当する `Wallet` が存在する場合は取得し、
        # 存在しない場合は新しく作成してタプル (wallet, created) を返す
        wallet = Wallet.objects.get_or_create(member=request.user.member)

        # `get_or_create` は (walletオブジェクト, 作成されたかどうかのブール値) のタプルを返す
        # そのため、walletがタプルの場合、walletオブジェクトのみ取得する
        wallet = wallet[0] if isinstance(wallet, tuple) else wallet

        # ユーザーの `Wallet` 情報をテンプレートに渡して表示する
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

# ---------------------------------------------------------------------
# 追加ポイント確認ビュー
# ---------------------------------------------------------------------
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
    
# ---------------------------------------------------------------------
# 商品検索ビュー
# ---------------------------------------------------------------------
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
    
# ---------------------------------------------------------------------
# 商品登録用のビュー
# ユーザーがログインしている場合のみアクセス可能。
# ---------------------------------------------------------------------
class ProductCreateView(LoginRequiredMixin, View):
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

# ---------------------------------------------------------------------
# 商品詳細ビュー
# ログインユーザーが出品者なら編集画面へ、そうでなければ購入画面へ遷移。
# ---------------------------------------------------------------------
class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)  # 商品を取得

        # ログインユーザーが出品者の場合
        if request.user.is_authenticated and product.seller == request.user:
            return redirect(reverse('member:product_edit', args=[product.id]))

        # ログインユーザーが出品者でない場合（購入画面へ）
        return redirect(reverse('member:product_purchase', args=[product.id]))

# ---------------------------------------------------------------------
# 商品編集ビュー
# ログインユーザーが出品者の場合のみアクセス可能。
# ---------------------------------------------------------------------
class ProductEditView(LoginRequiredMixin, UpdateView):
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

# ---------------------------------------------------------------------
# 商品購入ビュー
# ---------------------------------------------------------------------
class ProductPurchaseView(LoginRequiredMixin, View):
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
        product = Product.objects.get(id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        member = Member.objects.get(member_num=request.user.member_num)

        # カートに商品を追加
        Cart.objects.create(member=member, product=product, quantity=quantity)

        return redirect(reverse('member:cart_confirmation'))
    
# ---------------------------------------------------------------------
# カート確認画面ビュー
# ---------------------------------------------------------------------
class CartConfirmationView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = Cart.objects.filter(member=request.user)
        return render(request, 'products/cart_confirmation.html', {
            'cart_items': cart_items,
        })

    def post(self, request):
        # カート内の商品を確定して注文番号を生成
        cart_items = Cart.objects.filter(user=request.user)
        order_number = f"ORD-{uuid.uuid4().hex[:8]}"

        for item in cart_items:
            # 必要に応じてOrderモデルで保存
            item.delete()  # カートから削除

        return render(request, 'products/order_success.html', {
            'order_number': order_number,
        })
    

# ====================================================================================================
# ===== スケジュールアプリ
# ====================================================================================================

class UserScheduleListView(ListView):
    """ユーザーのスケジュール一覧を曜日ごとに表示"""
    model = UserSchedule
    template_name = 'schedule/user_schedule_list.html'
    context_object_name = 'user_schedules'

    def get_queryset(self):
        """ログインユーザーのスケジュールを取得"""
        return UserSchedule.objects.filter(member=self.request.user) 

    def get_context_data(self, **kwargs):
        """曜日ごとにスケジュールを分類してコンテキストに追加"""
        context = super().get_context_data(**kwargs)

        # 曜日ごとにスケジュールを分類する辞書（キー: 英数字曜日, 値: スケジュールリスト）
        schedules_by_day = {
            "mon": [], "tue": [], "wed": [], "thu": [], "fri": [], "sat": [], "sun": [],
        }

        # ユーザーのスケジュールを曜日ごとに分類
        for user_schedule in context['user_schedules']:
            day_of_week = user_schedule.get_day_of_week_display()  # 数字から英数字に変換
            day_of_week = self.convert_day_to_english(day_of_week)  # 英語表記に変換
            if day_of_week in schedules_by_day:
                schedules_by_day[day_of_week].append(user_schedule)

        # コンテキストに追加
        context['schedules_by_day'] = schedules_by_day
        return context

    def convert_day_to_english(self, day_of_week):
        """日本語の曜日を英語の曜日に変換"""
        day_map = {
            '月': 'mon',
            '火': 'tue',
            '水': 'wed',
            '木': 'thu',
            '金': 'fri',
            '土': 'sat',
            '日': 'sun',
        }
        return day_map.get(day_of_week, '')
    
# 予定選択
class EventSelectView(ListView):
    """予定の選択画面（検索機能付き）"""
    model = Event  # Eventモデルを使用
    template_name = 'schedule/user_schedule_select.html'  # 使用するテンプレート
    context_object_name = 'schedules'  # コンテキスト変数名として 'schedules' を指定

    def get_queryset(self):
        """検索フォームの値を取得し、フィルタリングして予定を取得"""
        queryset = Event.objects.all()  # 全てのEventを取得

        # ログインユーザーに紐づくMemberを取得
        member = Member.objects.get(member_num=self.request.user.member_num)

        # URLパラメータから曜日を取得（例: 'mon'）
        day_of_week_str = self.kwargs.get('day')
        
        # 英語の曜日を数字に変換する辞書
        days_map = {
            'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7
        }
        
        # 曜日を数字に変換
        day_of_week = days_map.get(day_of_week_str)

        # すでに選択済みの予定を取得（UserScheduleから）
        selected_schedules = UserSchedule.objects.filter(
            member=member,  # ログインユーザーのMemberを指定
            day_of_week=day_of_week  # 選択された曜日を指定
        ).values_list('schedule_id', flat=True)  # 予定IDのリストを取得

        # 既に選択されている予定を除外
        queryset = queryset.exclude(id__in=selected_schedules)

        # 検索キーワードがあればフィルタリング
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)  # タイトルにキーワードが含まれている予定をフィルタリング

        # カテゴリーが選択されていればフィルタリング
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # 重要度が選択されていればフィルタリング
        importance_id = self.request.GET.get('importance')
        if importance_id:
            queryset = queryset.filter(importance_id=importance_id)

        return queryset  # 最終的にフィルタリングされた予定リストを返す

    def get_context_data(self, **kwargs):
        """カテゴリー・重要度リストをテンプレートに渡す"""
        context = super().get_context_data(**kwargs)  # 親クラスのcontextを取得
        context['categories'] = Category.objects.all()  # すべてのカテゴリを取得してcontextに追加
        context['importances'] = Importance.objects.all()  # すべての重要度を取得してcontextに追加
        day_of_week_str = self.kwargs.get('day')  # URLパラメータから曜日を取得
        japanese_day = self.convert_day_to_japanese(day_of_week_str)  # 日本語の曜日に変換
        context['japanese_day'] = japanese_day  # コンテキストに追加
        return context

    def convert_day_to_japanese(self, day_of_week):
        """英語の曜日を日本語の曜日に変換"""
        day_map = {
            'mon': '月',
            'tue': '火',
            'wed': '水',
            'thu': '木',
            'fri': '金',
            'sat': '土',
            'sun': '日',
        }
        return day_map.get(day_of_week, '')

    def post(self, request, *args, **kwargs):
        """選択した予定を登録する処理"""
        # フォームから選択された予定のIDリストを取得
        selected_schedule_ids = request.POST.getlist('selected_schedules')  # 'selected_schedules'のパラメータをリストで取得
        
        # URLパラメータから曜日を取得
        day_of_week_str = kwargs.get('day')
        
        # 英語の曜日を数字に変換する辞書
        days_map = {
            'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7
        }
        
        # 曜日を数字に変換
        day_of_week = days_map.get(day_of_week_str)

        if not day_of_week:
            # 不正な曜日の場合、エラーページにリダイレクト
            return redirect('error_page')  # 適切なエラーページを作成してリダイレクトします

        # ログインユーザーに紐づくMemberを取得
        member = Member.objects.get(member_num=request.user.member_num)

        if selected_schedule_ids:
            # 選択した予定IDがあれば、UserScheduleに登録
            for schedule_id in selected_schedule_ids:
                try:
                    schedule = Event.objects.get(id=schedule_id)  # 予定IDからEventを取得
                except Event.DoesNotExist:
                    # 該当する予定が存在しない場合はスキップ
                    continue

                # UserScheduleに選択した予定を登録
                UserSchedule.objects.create(
                    member=member,  # メンバー情報を指定
                    schedule=schedule,  # 選択した予定を指定
                    day_of_week=day_of_week  # 数字で曜日を登録
                )

        # 登録後、スケジュール一覧ページへリダイレクト
        return redirect('member:user_schedule_list')  # ユーザーのスケジュール一覧ページにリダイレクト
