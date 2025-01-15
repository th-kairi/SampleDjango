from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# === account関連 ==================================================================
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

# Member用のAdmin
class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ['name', 'email', 'is_password_encrypted', 'membership_status']
    list_filter = ['is_password_encrypted', 'membership_status']
    search_fields = ['email', 'name']
    
    # `groups`、`user_permissions`、`date_joined` を非表示
    exclude = ('groups', 'user_permissions', 'date_joined')

# Employee用のAdmin
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['name', 'email', 'is_password_encrypted', 'division', 'team', 'position']
    list_filter = ['is_password_encrypted', 'division', 'team', 'position']
    search_fields = ['email', 'name', 'division__name', 'team__name', 'position__name']
    
    # `groups`、`user_permissions`、`date_joined` を非表示
    exclude = ('groups', 'user_permissions', 'date_joined')

# 管理画面登録
admin.site.register(position)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Employee, EmployeeAdmin)

# === 職員機能関連
class MemberMedalAdmin(admin.ModelAdmin):
    list_display = ['member', 'medal', 'acquisition_date', 'expiration_date']
    search_fields = ['member__name', 'medal__name']
    list_filter = ['medal', 'acquisition_date']

class MedalAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    
admin.site.register(Medal, MedalAdmin)
admin.site.register(MemberMedal, MemberMedalAdmin)