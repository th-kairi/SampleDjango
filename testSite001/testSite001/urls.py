from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('', include('main.urls')),
    path('employee', include('employee.urls')),
    path('member', include('member.urls')),

]
