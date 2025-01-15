from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.views import View
from .forms import MemberSelectionForm
from main.models import *
from django.core.exceptions import ObjectDoesNotExist

class IndexView(TemplateView):
    template_name = 'employee/index.html'  # 使用するテンプレートファイル

class MemberSelectionView(View):
    def get(self, request):
        form = MemberSelectionForm()  # フォームをインスタンス化
        return render(request, 'employee/select_member.html', {'form': form})

    def post(self, request):
        form = MemberSelectionForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            print("=====================================================")
            print(member)
            print(member.name)
            print(member.email)
            print(member.member_num)
            print(member.id)
            print("=====================================================")
            if member:  # member が存在することを確認
                # 会員選択後に勲章選択画面にリダイレクト
                return redirect('medal_register:select_medals', member_id=member.id)
            else:
                # member が None の場合はエラーメッセージを表示
                messages.error(request, "会員が正しく選択されていません。")
                return render(request, 'employee/select_member.html', {'form': form})
        return render(request, 'employee/select_member.html', {'form': form})

class MedalSelectView(View):
    def get(self, request, member_id):
        # member_id を元に会員を取得
        member = Member.objects.get(id=member_id)

        # 会員が既に持っている勲章を取得
        existing_medals = MemberMedal.objects.filter(member=member).values_list('medal', flat=True)

        # 既に持っていない勲章のみを表示
        available_medals = Medal.objects.exclude(id__in=existing_medals)

        return render(request, 'employee/medal_select.html', {'available_medals': available_medals, 'member': member})

    def post(self, request, member_id):
        member = Member.objects.get(id=member_id)
        selected_medals = request.POST.getlist('medals')  # 複数選択のためgetlistを使用

        # 勲章を会員に登録
        for medal_id in selected_medals:
            medal = Medal.objects.get(id=medal_id)
            MemberMedal.objects.create(member=member, medal=medal)

        # 勲章登録完了後に遷移する場所
        return redirect('employee:medal_member')