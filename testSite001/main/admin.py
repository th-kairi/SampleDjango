from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# import * とすることでmodels.pyで定義した全てのモデルをインポートする
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['member_num', 'name', 'email', 'is_password_encrypted']
    list_filter = ['is_password_encrypted']
    search_fields = ['email', 'name']

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(position)
admin.site.register(Employee)
admin.site.register(Member)
