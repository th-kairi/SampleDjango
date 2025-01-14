from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'member/index.html'  # 使用するテンプレートファイル
    