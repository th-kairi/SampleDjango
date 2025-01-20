from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # 標準の管理者ページ
    path('accounts/', include('accounts.urls')), # ログイン周り（CUstomUser周り）
    path('', include('main.urls')), # 管理アプリ
    path('employee/', include('employee.urls')), # employeeアプリ
    path('member/', include('member.urls')), # memberアプリ
    path('staff/', include('staff.urls')),  # staffアプリ

]

# メディアファイルへのアクセスを許可
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)