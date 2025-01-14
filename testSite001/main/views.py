# main/views.py
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'main/index.html'  # 使用するテンプレートファイル
    