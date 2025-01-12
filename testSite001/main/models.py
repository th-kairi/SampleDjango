from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.

# 役職
class position(models.Model):
    CATEGORY_TYPE_CHOICES = [('部署', '部署'), ('課', '課'), ('役職', '役職')]
    cd = models.CharField(verbose_name="コード", max_length=10, primary_key=True)
    name = models.CharField(verbose_name="名称",max_length=20)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)

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
    division = models.ForeignKey(position, verbose_name="部署", on_delete=models.CASCADE, limit_choices_to={'type': '部署'}, related_name='users_in_division')
    team = models.ForeignKey(position, verbose_name="課", on_delete=models.CASCADE, limit_choices_to={'type': '課'}, related_name='users_in_team')
    position = models.ForeignKey(position, verbose_name="役職", on_delete=models.CASCADE, limit_choices_to={'type': '役職'}, related_name='users_in_position')
    # passwordは標準の機能を利用
    zip_code = models.CharField(verbose_name="郵便番号", max_length=8)
    address	= models.CharField(verbose_name="住所", max_length=50)

    class Meta:
        verbose_name_plural = "職員"

    def __str__(self):
        return f"{self.name}({self.job_title})"

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