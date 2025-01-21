from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.views import View
from .forms import MemberSelectionForm
from main.models import *

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
            if member:  # member が存在することを確認
                # 会員選択後に勲章選択画面にリダイレクト
                return redirect('employee:acquired_medals', member_num=member.member_num)
            else:
                # member が None の場合はエラーメッセージを表示
                messages.error(request, "会員が正しく選択されていません。")
                return render(request, 'employee/select_member.html', {'form': form})
        return render(request, 'employee/select_member.html', {'form': form})
    
class AcquiredMedalsView(View):
    def get(self, request, member_num):
        # 会員を取得
        member = Member.objects.get(member_num=member_num)

        # 会員が取得した勲章を取得
        acquired_medals = MemberMedal.objects.filter(member=member)

        return render(request, 'employee/acquired_medals.html', {
            'member': member,
            'acquired_medals': acquired_medals
        })
    
class MedalDetailView(View):
    def get(self, request, member_num, medal_id):
        # 会員と勲章のデータを取得
        member = Member.objects.get(member_num=member_num)
        medal = Medal.objects.get(id=medal_id)

        # すでに取得しているかをチェック
        already_acquired = MemberMedal.objects.filter(member=member, medal=medal).exists()

        return render(request, 'employee/medal_detail.html', {
            'member': member,
            'medal': medal,
            'already_acquired': already_acquired
        })

    def post(self, request, member_num, medal_id):
        # 会員と勲章のデータを取得
        member = Member.objects.get(member_num=member_num)
        medal = Medal.objects.get(id=medal_id)

        # すでに取得している場合は処理しない
        if MemberMedal.objects.filter(member=member, medal=medal).exists():
            return redirect('employee:acquired_medals', member_num=member.member_num)

        # 取得日と期限をフォームから取得
        acquisition_date = request.POST.get('acquisition_date')
        expiration_date = request.POST.get('expiration_date')

        # MemberMedalにデータを保存（会員と勲章の関連付け）
        MemberMedal.objects.create(
            member=member,
            medal=medal,
            acquisition_date=acquisition_date,
            expiration_date=expiration_date
        )

        # 勲章を取得した会員の一覧画面に遷移
        return redirect('employee:acquired_medals', member_num=member.member_num)

class MedalSelectView(View):
    def get(self, request, member_num):
        # 会員情報を取得
        member = Member.objects.get(member_num=member_num)

        # 会員が既に取得している勲章のIDを取得
        existing_medals = MemberMedal.objects.filter(member=member).values_list('medal_id', flat=True)

        # 既に持っていない勲章のみを表示
        available_medals = Medal.objects.exclude(id__in=existing_medals)

        # 会員が取得した勲章を格納する辞書（キー: medal.id, 値: 取得済みか否か）
        medals_status = {medal.id: True for medal in MemberMedal.objects.filter(member=member)}

        return render(request, 'employee/medal_select.html', {
            'member': member,
            'available_medals': available_medals,
            'medals_status': medals_status  # 勲章の取得状態を渡す
        })
    
    def post(self, request, member_num):
        # member_num を使って会員を取得
        member = Member.objects.get(member_num=member_num)
        selected_medals = request.POST.getlist('medals')

        for medal_id in selected_medals:
            medal = Medal.objects.get(id=medal_id)
            MemberMedal.objects.create(member=member, medal=medal)

        messages.success(request, f'{len(selected_medals)} 個の勲章を {member.name} に登録しました。')
        return redirect('employee:select_member')

