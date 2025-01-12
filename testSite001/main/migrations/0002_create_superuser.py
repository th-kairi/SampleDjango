from django.db import migrations
from django.contrib.auth.models import User
from main.models import CustomUser  # CustomUser モデルをインポート

def create_superuser(apps, schema_editor):
    # スーパーユーザーの情報を設定
    CustomUser.objects.create_superuser(
        username='admin',
        email='admin@mail.com',
        password='admin'  # セキュアなパスワードを使用する
    )

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),  # 依存関係を正しく設定
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
