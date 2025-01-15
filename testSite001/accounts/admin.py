from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# import * とすることでmodels.pyで定義した全てのモデルをインポートする
from main.models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['name', 'email', 'is_password_encrypted']
    list_filter = ['is_password_encrypted']
    search_fields = ['email', 'name']

class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ['name', 'email', 'is_password_encrypted']
    list_filter = ['is_password_encrypted']
    search_fields = ['email', 'name']
    
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['name', 'email', 'is_password_encrypted']
    list_filter = ['is_password_encrypted','division', 'team', 'position']
    search_fields = ['email', 'name', 'division', 'team', 'position']

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(position)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Member, MemberAdmin)
