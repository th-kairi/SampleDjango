from django.db import migrations
from django.contrib.auth.models import User
from main.models import *

def create_superuser(apps, schema_editor):
    # スーパーユーザーの情報を設定
    user = CustomUser.objects.create_superuser(
        username='admin',
        name='administraotr',
        email='admin@mail.com',
        password='admin',  # セキュアなパスワードを使用する
        is_password_encrypted=True,
    )
    user.is_staff = True  # スタッフ権限も付与
    user.is_superuser = True  # スーパーユーザーとして設定
    user.save()

    employee = Employee.objects.create_user(
        username='employee',
        name='employee',
        email='employee@mail.com',
        password='employee',  # セキュアなパスワードを使用する
        is_password_encrypted=True,
    )
    employee.save()

    member = Member.objects.create_user(
        username='member',
        name='member',
        email='member@mail.com',
        password='member',  # セキュアなパスワードを使用する
        is_password_encrypted=True,
    )
    member.save()
    
    member = Staff.objects.create_user(
        username='staff',
        name='staff',
        email='staff@mail.com',
        password='staff',  # セキュアなパスワードを使用する
        is_password_encrypted=True,
    )
    member.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),  # 依存関係を正しく設定
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
