from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ph9nn=73+&3(lh)s(apvgg%-@f^^$^w4bc@#rhyp)^g5#%hini'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 追加したアプリケーションを設定する（インストールする）
    'accounts.apps.AccountsConfig',
    'main.apps.MainConfig',
    'member.apps.MemberConfig',
    'employee.apps.EmployeeConfig',

    # 自動でカンマ区切りにするアプリ
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'testSite001.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # mainアプリケーション内のtemplatesディレクトリを指定
            # この設定をする事で別アプリケーションからbase.htmlを参照してサイトをデザインする事ができる
            BASE_DIR / 'main/templates',  # BASE_DIR はプロジェクトのルートディレクトリ
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'testSite001.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/


# 使用言語とタイムゾーンを日本仕様にする（P106）
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# staticファイルを読み込めるように設定する
# 教科書P340,341
import os # <- 一番上に書く
STATICFILES_DIRS=(
    os.path.join(BASE_DIR, 'static'),
)

# 画像ファイルを表示・保存する為の設定
# mediaのURLを登録
MEDIA_URL = '/media/'
# mediaフォルダの場所（BASE_DIR以下のmediaを登録）
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ログインに使うユーザーモデルを指定
AUTH_USER_MODEL = 'main.CustomUser'
# ログイン後のリダイレクト先
LOGIN_REDIRECT_URL = '/'

# ログイン時にメールアドレスとNameどちらでも認証できるようにカスタムバックエンドを使う
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # デフォルトの認証バックエンド
    'testSite001.backends.CustomBackend',  # カスタムバックエンド
]

# 送信メールをターミナルに表示する設定（デバッグ用）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'