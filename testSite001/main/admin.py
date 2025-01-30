from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# === account関連 ==================================================================
# positionモデルを管理画面に登録
class PositionAdmin(admin.ModelAdmin):
    list_display = ('cd', 'name', 'name_en', 'type')
    search_fields = ('cd', 'name', 'name_en')
    
admin.site.register(position, PositionAdmin)

# CustomUser用のAdmin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['member_num','name', 'email', 'is_password_encrypted', 'is_active', 'is_staff']
    list_filter = ['is_password_encrypted', 'is_active', 'is_staff']
    search_fields = ['email', 'name']
    
    # フィールドの表示順序や構成を調整
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    # `groups`、`user_permissions`、`date_joined` を非表示
    exclude = ('groups', 'user_permissions', 'date_joined')

admin.site.register(CustomUser, CustomUserAdmin)

# Member用のAdmin
class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ['name', 'email', 'is_password_encrypted', 'membership_status']
    list_filter = ['is_password_encrypted', 'membership_status']
    search_fields = ['email', 'name']
    
    # `groups`、`user_permissions`、`date_joined` を非表示
    exclude = ('groups', 'user_permissions', 'date_joined')

admin.site.register(Member, MemberAdmin)


# Employee用のAdmin
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['name', 'email', 'is_password_encrypted', 'division', 'team', 'position']
    list_filter = ['is_password_encrypted', 'division', 'team', 'position']
    search_fields = ['email', 'name', 'division__name', 'team__name', 'position__name']
    
    # `groups`、`user_permissions`、`date_joined` を非表示
    exclude = ('groups', 'user_permissions', 'date_joined')
    
admin.site.register(Employee, EmployeeAdmin)

# === 職員機能関連
class MemberMedalAdmin(admin.ModelAdmin):
    list_display = ['member', 'medal', 'acquisition_date', 'expiration_date']
    search_fields = ['member__name', 'medal__name']
    list_filter = ['medal', 'acquisition_date']
    
admin.site.register(MemberMedal, MemberMedalAdmin)

class MedalAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    
admin.site.register(Medal, MedalAdmin)


# === staff関連 ==================================================================
# Rankモデルを管理画面に登録
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
admin.site.register(Rank, RankAdmin)

# Staffモデルを管理画面に登録
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'division', 'team', 'position', 'hire_date', 'phone_number')
    search_fields = ('name', 'email')
    list_filter = ('division', 'team', 'position')
    ordering = ('name',)

    list_display = ['name', 'email', 'is_password_encrypted']
    list_filter = ['is_password_encrypted']
    search_fields = ['email', 'name']
    
    # `groups`、`user_permissions`、`date_joined` を非表示
    exclude = ('groups', 'user_permissions', 'date_joined')
    
admin.site.register(Staff, StaffAdmin)

# ShiftRequestモデルを管理画面に登録
class ShiftRequestAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'start_time', 'end_time', 'is_submitted')
    list_filter = ('is_submitted', 'staff')
    search_fields = ('staff__name', 'date')
    ordering = ('date',)
    
admin.site.register(ShiftRequest, ShiftRequestAdmin)

# ShiftScheduleモデルを管理画面に登録
class ShiftScheduleAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'start_time', 'end_time', 'is_confirmed')
    list_filter = ('is_confirmed', 'staff')
    search_fields = ('staff__name', 'date')
    ordering = ('date',)


# ====================================================================================================
# ===== フリマアプリ
# ====================================================================================================

# 商品モデルの管理画面カスタマイズ
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'price', 'created_at')  # 一覧画面で表示する項目
    list_filter = ('seller', 'created_at')  # フィルタリングオプション
    search_fields = ('name', 'description', 'seller__name')  # 検索対象項目
    ordering = ('-created_at',)  # ソート順
    date_hierarchy = 'created_at'  # 日付階層ナビゲーション
admin.site.register(Product, ProductAdmin)

# 商品画像の管理画面カスタマイズ
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'uploaded_at')  # 一覧画面で表示する項目
    list_filter = ('product',)  # フィルタリングオプション
    search_fields = ('product__name',)  # 検索対象項目
admin.site.register(ProductImage, ProductImageAdmin)

# ウォレットモデルの管理画面カスタマイズ
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'balance')  # 一覧画面で表示する項目
    search_fields = ('member__name', 'member__member_num')  # 検索対象項目
    list_filter = ('balance',)  # フィルタリングオプション
    ordering = ('-balance',)  # ソート順
admin.site.register(Wallet, WalletAdmin)

# 注文モデルの管理画面カスタマイズ
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_price', 'created_at')  # 一覧画面で表示する項目
    list_filter = ('buyer', 'created_at')  # フィルタリングオプション
    search_fields = ('buyer__name', 'buyer__member_num')  # 検索対象項目
    date_hierarchy = 'created_at'  # 日付階層ナビゲーション
admin.site.register(Order, OrderAdmin)

# 
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')  # 一覧画面で表示する項目
    search_fields = ('order__buyer__name', 'product__name')  # 検索対象項目
    list_filter = ('product',)  # フィルタリングオプション
admin.site.register(OrderItem, OrderItemAdmin)

# まとめて注文をする際に利用する一時モデルの管理画面カスタマイズ
admin.site.register(Cart)


# ====================================================================================================
# ===== スケジュールアプリ
# ====================================================================================================

# Categoryの管理画面カスタマイズ
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 一覧に表示するフィールド
    search_fields = ('name',)  # 検索フィールド（カテゴリ名で検索）
    ordering = ('name',)  # 並び順をカテゴリ名でソート
admin.site.register(Category, CategoryAdmin)

# Importanceの管理画面カスタマイズ
class ImportanceAdmin(admin.ModelAdmin):
    list_display = ('level',)  # 一覧に表示するフィールド
    search_fields = ('level',)  # 検索フィールド（重要度レベルで検索）
    ordering = ('level',)  # 並び順を重要度レベルでソート
admin.site.register(Importance, ImportanceAdmin)

# スケジュールの管理画面カスタマイズ
class ScheduleAdmin(admin.ModelAdmin):
    # 管理画面で表示するフィールド
    list_display = ('title', 'image', 'created_at', 'is_completed', 'updated_at')  # タイトル、作成日時、完了状態、更新日時を表示
    
    # 完了状態や作成日時で絞り込みができるようにする
    list_filter = ('is_completed', 'created_at')
    
    # タイトルや詳細で検索できるようにする
    search_fields = ('title', 'description')
    
    # 編集可能なフィールドを設定（完了状態は管理画面で直接変更可能）
    list_editable = ('is_completed',)

    # 作成日時と更新日時を管理画面で見やすく設定
    ordering = ('-created_at',)  # 新しい順に並べる
    

    # 詳細画面でのフィールド順を指定
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'description', 'category', 'importance', 'is_completed')
        }),
        ('日時情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # 隠すクラス（必要に応じて表示）
        }),
    )

    # 詳細画面で表示するフィールドの順番を指定
    readonly_fields = ('created_at', 'updated_at')  # 作成日時と更新日時は読み取り専用

    # フォームでの並び順を指定（必要に応じて）
    save_on_top = True  # 「保存」ボタンを上部に配置
admin.site.register(Schedule, ScheduleAdmin)

# UserSchedule管理用クラス
class UserScheduleAdmin(admin.ModelAdmin):
    # 管理画面に表示するフィールドを指定
    list_display = ('Member', 'schedule', 'day_of_week', 'is_completed')  # 必要なフィールドを追加
    search_fields = ('Member__name', 'schedule__title')  # メンバー名や予定タイトルで検索可能にする
    list_filter = ('day_of_week', 'is_completed')  # 曜日や完了状態でフィルタリングできるようにする

    # 編集フォームでのフィールド配置
    fieldsets = (
        (None, {
            'fields': ('Member', 'schedule', 'day_of_week', 'is_completed')
        }),
    )
    def get_member_name(self, obj):
        """UserSchedule インスタンスの member の name を表示"""
        return obj.member.name  # 'member' フィールドに関連する 'name' を表示
    
    get_member_name.short_description = 'Member Name'  # ヘッダー名を変更

    search_fields = ('member__name', 'schedule__title')  # メンバー名や予定タイトルで検索可能にする
    list_filter = ('day_of_week', 'is_completed')  # 曜日や完了状態でフィルタリングできるようにする

    fieldsets = (
        (None, {
            'fields': ('Member', 'schedule', 'day_of_week', 'is_completed')
        }),
    )

# UserScheduleモデルを管理画面に登録
admin.site.register(UserSchedule, UserScheduleAdmin)
