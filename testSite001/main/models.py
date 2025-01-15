from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.

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
        return f"{self.name}({self.membership_status})"
    

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