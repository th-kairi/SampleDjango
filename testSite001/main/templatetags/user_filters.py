from django import template

register = template.Library()

@register.filter
def is_admin(user):
    return user.is_superuser  # 管理者かどうかを判定

@register.filter
def is_member(user):
    return hasattr(user, 'member')  # Memberとしての関連があるか確認

@register.filter
def is_employee(user):
    return hasattr(user, 'employee')  # Employeeとしての関連があるか確認

@register.filter
def is_staff(user):
    return hasattr(user, 'staff')  # Staffとしての関連があるか確認
