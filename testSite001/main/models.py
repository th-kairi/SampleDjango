from django.db import models
from django.contrib.auth.models import AbstractUser
import random


# 役職
class position(models.Model):
    CATEGORY_TYPE_CHOICES = [('部署', '部署'), ('課', '課'), ('役職', '役職')]
    cd = models.CharField(verbose_name="コード", max_length=10, primary_key=True)
    name = models.CharField(verbose_name="名称",max_length=20)
    name_en = models.CharField(verbose_name="名称(EN)",max_length=20)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES, blank=True, null=True)

    # 役職モデルの参照設定
    class Meta:
        verbose_name_plural = "役職"
    def __str__(self):
        # return f"{self.name}({self.cd})"
        return f"{self.name}"

# カスタムユーザー用
# 会員番号の採番乱数関数
def random_num():
    return str(random.randint(1000000000000,10000000000000)) # (1*10^12, 1*10^13)

# カスタムユーザーモデル
class CustomUser(AbstractUser):
    member_num = models.BigIntegerField(verbose_name="会員番号",
                                         primary_key=True,
                                         default=random_num # 乱数関数
                                         )
    name = models.CharField(verbose_name="氏名", max_length=20)
    email   = models.EmailField(verbose_name="メールアドレス", unique=True)
    is_password_encrypted = models.BooleanField(default=False, verbose_name="パスワード暗号化フラグ")

    # メールアドレスでログインする
    USERNAME_FIELD = 'email' # 標準のユーザー名を「email」と同じする
    REQUIRED_FIELDS = ['username']
    
    # デフォルトのログイン用ユーザー名を無効化する
    username = models.CharField(verbose_name="ユーザー名", 
                                max_length=20,
                                blank=True, null=True
                                )
    # CustomUserが参照されたときに返す値を設定
    class Meta:
        verbose_name_plural = "カスタムユーザー"
    def __str__(self):
        return f"{self.name}({self.email})"
    
    # def save(self, *args, **kwargs):
    #     # パスワードが暗号化されている場合は、フラグをTrueに設定
    #     if self.password and not self.is_password_encrypted:
    #         self.is_password_encrypted = True
    #     super().save(*args, **kwargs)
    
# 職員モデル（CustomUserを継承）
class Employee(CustomUser):
    division = models.ForeignKey(position,
                                 verbose_name="部署",
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'type': '部署'}, 
                                 related_name='users_in_division',
                                 blank=True,
                                 null=True)
    team = models.ForeignKey(position, 
                             verbose_name="課", 
                             on_delete=models.CASCADE, 
                             limit_choices_to={'type': '課'}, 
                             related_name='users_in_team',
                             blank=True,
                             null=True)
    position = models.ForeignKey(position, 
                                 verbose_name="役職", 
                                 on_delete=models.CASCADE, 
                                 limit_choices_to={'type': '役職'}, 
                                 related_name='users_in_position',
                                 blank=True,
                                 null=True)
    # passwordは標準の機能を利用
    zip_code = models.CharField(verbose_name="郵便番号", max_length=8, blank=True, null=True)
    address	= models.CharField(verbose_name="住所", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "職員"

    def __str__(self):
            # 部署、課、役職がNoneまたは空文字の場合は空白をセット
            division_name = self.division.name if self.division and self.division.name else ''
            team_name = self.team.name if self.team and self.team.name else ''
            position_name = self.position.name if self.position and self.position.name else ''
            
            # すべて空の場合は括弧を表示しないようにする
            names = [division_name, team_name, position_name]
            non_empty_names = [name for name in names if name]  # 空文字ではない名前だけをリストに追加

            # 名前が1つでもあればそれを表示、なければ空文字を返す
            if non_empty_names:
                return f"{self.name} ({' '.join(non_empty_names)})"
            else:
                return self.name

# 会員モデル（CustomUserを継承）
class Member(CustomUser):
    subscription_date = models.DateField(verbose_name="加入日", blank=True, null=True)
    membership_status = models.CharField(verbose_name="会員ステータス", 
                                         max_length=20, 
                                         choices=[('active', 'アクティブ'), ('inactive', '非アクティブ')],
                                         default='active')
    points	= models.IntegerField(verbose_name="保有ポイント", default=0)

    class Meta:
        verbose_name_plural = "会員"

    def __str__(self):
        return f"{self.name}({self.member_num})"
    
    def save(self, *args, **kwargs):
        # 会員が保存された後にWalletを作成
        is_new = self.pk is None  # 新しいインスタンスかどうかを確認
        super().save(*args, **kwargs)
        if is_new:
            Wallet.objects.get_or_create(member=self)  # Walletが存在しない場合に作成

# 勲章モデル
class Medal(models.Model):
    name = models.CharField(max_length=100, verbose_name="勲章名")
    image = models.ImageField(upload_to='medals/', verbose_name="アイコン", blank=True, null=True)  # 勲章のアイコン画像
    description = models.TextField(verbose_name="勲章の説明")
    requirements = models.TextField(max_length=400,verbose_name="授与条件", blank=True, null=True)  # 授与条件
    eligible_for = models.TextField(max_length=100, verbose_name="対象者", blank=True, null=True)  # 対象者
    awarding_method = models.TextField(max_length=300, verbose_name="授与方法", blank=True, null=True)  # 授与方法

    class Meta:
        verbose_name_plural = "勲章"

    def __str__(self):
        return self.name


# 会員が取得した勲章
class MemberMedal(models.Model):
    member = models.ForeignKey(Member, verbose_name="会員", on_delete=models.CASCADE)  # 会員
    medal = models.ForeignKey(Medal, verbose_name="勲章", on_delete=models.CASCADE)  # 勲章
    acquisition_date = models.DateField(verbose_name="取得日")  # 取得日
    expiration_date = models.DateField(verbose_name="有効期限", null=True, blank=True)  # 有効期限（無期限の場合はNULL）

    def __str__(self):
        return f"{self.member.name} - {self.medal.name}"

    class Meta:
        verbose_name_plural = "会員勲章"
        unique_together = ('member', 'medal')  # 同じ会員が同じ勲章を2度取得できないように設定

# ランクモデル
class Rank(models.Model):
    name = models.CharField(verbose_name="ランク名", max_length=50)  # ランク名
    description = models.TextField(verbose_name="ランクの説明", blank=True, null=True)  # ランクの説明

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ランク"

# スタッフモデル（CustomUserを継承）
class Staff(CustomUser):
    division = models.ForeignKey(position, verbose_name="部署",
                                 on_delete=models.CASCADE, 
                                 limit_choices_to={'type': '部署'}, 
                                 related_name='staff_in_division',
                                 blank=True, null=True)
    team = models.ForeignKey(position, verbose_name="課",
                              on_delete=models.CASCADE,
                              limit_choices_to={'type': '課'}, 
                              related_name='staff_in_teasm',
                              blank=True, null=True)
    position = models.ForeignKey(position, verbose_name="役職", 
                                 on_delete=models.CASCADE, 
                                 limit_choices_to={'type': '役職'}, 
                                 related_name='staff_in_position',
                                 blank=True, null=True)
    rank = models.ForeignKey(Rank, verbose_name="ランク",
                             on_delete=models.SET_NULL,
                             blank=True, null=True)
    hire_date = models.DateField(verbose_name="入社日", blank=True, null=True)
    phone_number = models.CharField(verbose_name="電話番号", max_length=15, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "スタッフ"

    def __str__(self):
        return f"({self.rank}){self.name}:{self.member_num}"

    class Meta:
        verbose_name_plural = "スタッフ"
        unique_together = ('division', 'team', 'position')  # 同じ部署、課、役職のスタッフを2度登録できないように設定
        permissions = [
            ('can_view_staff', 'Can view staff'),
        ]

# シフト希望モデル
class ShiftRequest(models.Model):
    staff = models.ForeignKey(Staff, verbose_name="スタッフ", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="希望日")
    start_time = models.TimeField(verbose_name="開始時間")
    end_time = models.TimeField(verbose_name="終了時間")
    is_submitted = models.BooleanField(default=False, verbose_name="提出済み")
    
    def __str__(self):
        return f"{self.staff.name} - {self.date} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name_plural = "シフト希望"
        unique_together = ('staff', 'date', 'start_time')  # 同一日に同じ時間帯の重複を防ぐ

# シフトスケジュールモデル
class ShiftSchedule(models.Model):
    staff = models.ForeignKey(Staff, verbose_name="スタッフ", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="勤務日")
    start_time = models.TimeField(verbose_name="勤務開始時間")
    end_time = models.TimeField(verbose_name="勤務終了時間")
    is_confirmed = models.BooleanField(default=False, verbose_name="確定済み")
    
    def __str__(self):
        return f"{self.staff.name} - {self.date} ({self.start_time} - {self.end_time})"

    class Meta:
        verbose_name_plural = "シフトスケジュール"
        unique_together = ('staff', 'date', 'start_time')  # 同一日に同じ時間帯の重複を防ぐ

# 商品モデル（商品画像は別モデルで管理）
class Product(models.Model):
    # 出品者を表す外部キー
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products", verbose_name="出品者")
    # 商品名を表す文字列フィールド
    name = models.CharField(max_length=255, verbose_name="商品名")
    # 商品の説明を表すテキストフィールド
    description = models.TextField(verbose_name="商品説明")
    # 商品の価格を表す整数フィールド
    price = models.IntegerField(verbose_name="価格")
    # 商品の作成日時を自動記録
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="出品日時")
    # 商品の更新日時を自動記録
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    is_sold_out = models.BooleanField(default=False, verbose_name="売り切れフラグ")  # 売り切れ状態を示すブール値

    class Meta:
        verbose_name_plural = "商品"
        ordering = ['-created_at']  # デフォルトで作成日時の降順に並べる

    def __str__(self):
        # 商品名と出品者の名前を文字列で返す
        return f"{self.name} - {self.seller.name}"


# 商品画像モデル（1商品に対して複数の画像を紐付け可能）
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="商品")
    # アップロードされた商品画像のパス（商品ごとにフォルダを分ける）
    image = models.ImageField(upload_to="products/images/", verbose_name="商品画像")
    # 商品画像のアップロード日時
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="アップロード日時")

    class Meta:
        verbose_name_plural = "商品画像"

    def __str__(self):
        # 管理画面などで画像の関連商品名を表示する
        return f"Image for {self.product.name}"


# 購入用ポイントを管理するウォレットモデル
class Wallet(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="wallet", verbose_name="会員")
    # 現在のポイント残高を格納するフィールド
    balance = models.PositiveIntegerField(default=0, verbose_name="ポイント残高")

    class Meta:
        verbose_name_plural = "ウォレット"

    def __str__(self):
        # 会員名とポイント残高を表示
        return f"{self.member.name}'s Wallet - {self.balance} points"

    # ポイントを追加するメソッド
    def add_points(self, amount):
        self.balance += amount
        self.save()

    # ポイントを使用するメソッド
    def use_points(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

# 商品購入時に一時的に作成するモデル
class Cart(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="会員")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    class Meta:
        verbose_name_plural = "カート"
    
    def __str__(self):
        return f"{self.member.name}'s Cart - {self.product.name} ({self.quantity})"
    

# 購入履歴を管理する注文モデル
class Order(models.Model):
    buyer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="orders", verbose_name="購入者")
    # 注文総額を格納
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="合計金額")
    # 注文日時
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="注文日時")

    class Meta:
        verbose_name_plural = "注文"
        ordering = ['-created_at']  # 最新の注文を上に表示

    def __str__(self):
        # 管理画面などで購入者名と注文IDを表示
        return f"Order #{self.id} by {self.buyer.name}"


# 注文に紐付く商品の詳細情報を管理するモデル
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="注文")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="商品")
    # 注文した商品の数量（1出品1在庫の場合、常に1となる）
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    class Meta:
        verbose_name_plural = "注文商品"

    def __str__(self):
        # 管理画面などで注文IDと商品名を表示
        return f"Order #{self.order.id} - {self.product.name}"
