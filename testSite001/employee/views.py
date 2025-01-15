from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.views import View
from .forms import MedalSelectionForm
from main.models import *
from django.core.exceptions import ObjectDoesNotExist

class IndexView(TemplateView):
    template_name = 'employee/index.html'  # 使用するテンプレートファイル


class MedalRegisterView(View):
    def get(self, request):
        # フォーム作成
        form = MedalSelectionForm()

        # 会員が既に持っている勲章のIDを取得
        member_id = request.GET.get('member')  # 例えば、会員を選択するためのフォームからmember IDを取得
        if member_id:
            member = Member.objects.get(id=member_id)
            # 会員が既に持っている勲章を除外
            existing_medals = MemberMedal.objects.filter(member=member).values_list('medal', flat=True)
            form.fields['medals'].queryset = Medal.objects.exclude(id__in=existing_medals)

        # Medal リストを渡す
        medals = Medal.objects.all()  # 勲章リストを取得

        return render(request, 'employee/medal_register.html', {'form': form, 'medals': medals})

    def post(self, request):
        form = MedalSelectionForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            medals = form.cleaned_data['medals']
            expiration_date = form.cleaned_data['expiration_date']

            # 既に会員が持っている勲章を除外
            existing_medals = MemberMedal.objects.filter(member=member).values_list('medal', flat=True)
            available_medals = Medal.objects.exclude(id__in=existing_medals)

            # 登録する勲章を選択
            for medal in medals:
                if medal not in available_medals:
                    continue  # 重複する勲章をスキップ

                MemberMedal.objects.create(
                    member=member,
                    medal=medal,
                    acquisition_date=form.cleaned_data.get('acquisition_date'),
                    expiration_date=expiration_date if expiration_date else None
                )

            messages.success(request, f'{len(medals)} 個の勲章を {member.name} に登録しました。')
            return redirect('employee:medal_register')

        return render(request, 'employee/medal_register.html', {'form': form})