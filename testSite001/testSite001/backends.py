from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    メールアドレスまたは名前でログイン可能にするカスタム認証バックエンド
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # email または name で認証
        try:
            user = User.objects.get(email=username)  # emailを使って取得
        except User.DoesNotExist:
            try:
                user = User.objects.get(name=username)  # nameを使って取得
            except User.DoesNotExist:
                return None  # email と name のどちらでもない場合

        if user.check_password(password):
            return user
        return None
