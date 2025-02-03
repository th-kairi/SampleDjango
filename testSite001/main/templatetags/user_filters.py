from django import template
from main.models import *

register = template.Library()

@register.filter
def is_admin(user):
    return user.is_superuser  # 管理者かどうかを判定

@register.filter
def is_member(user):
    return isinstance(user, Member)

@register.filter
def is_employee(user):
    return isinstance(user, Employee)

@register.filter
def is_staff(user):
    return isinstance(user, Staff)
