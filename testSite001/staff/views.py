# staff/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

class IndexView(TemplateView):
    template_name = 'staff/index.html'  # 使用するテンプレートファイル

# スタッフ一覧ページ
class StaffListView(ListView):
    model = Staff
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff_list'

# スタッフ詳細ページ
class StaffDetailView(DetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff'

# スタッフ追加ページ
class StaffCreateView(CreateView):
    model = Staff
    template_name = 'staff/staff_form.html'
    form_class = StaffForm
    success_url = reverse_lazy('staff:staff_list')

# シフト確認ページ（スタッフのシフト一覧）
class ShiftScheduleListView(ListView):
    model = ShiftSchedule
    template_name = 'staff/shift_schedule_list.html'
    context_object_name = 'shifts'

    def get_queryset(self):
        current_month = timezone.now().month
        current_year = timezone.now().year
        # 職員ユーザーがアクセスした場合
        if self.kwargs.get('staff_id') is None:
            return ShiftSchedule.objects.filter(
                date__year=current_year, 
                date__month=current_month
            ).select_related('staff')
        # スタッフが参照した場合（staff_idが渡された場合）
        else:
            staff = staff.objects.get(id=self.kwargs['staff_id'])
            return ShiftSchedule.objects.filter(
                staff=staff,
                date__year=current_year,
                date__month=current_month
            ).select_related('staff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = timezone.now().month
        context['current_year'] = timezone.now().year
        return context

# スタッフのシフト詳細ページ
class StaffShiftDetailView(DetailView):
    model = ShiftSchedule
    template_name = 'staff/staff_shift_detail.html'
    context_object_name = 'shift'

    def get_object(self):
        shift_id = self.kwargs.get('pk')  # URLのpkを取得
        return ShiftSchedule.objects.get(id=shift_id)  # 該当するシフト情報を取得
    
# シフトのスケジュールを表示
class ShiftScheduleView(View):
    def get(self, request, *args, **kwargs):
        # 現在の日付を取得
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        # 月の1日が何曜日かを計算
        first_day_of_month = timezone.datetime(current_year, current_month, 1)
        start_weekday = first_day_of_month.weekday()  # 0:月曜日, 6:日曜日

        # ログインユーザーのスタッフ情報を取得
        # staff = Staff.objects.filter(user=request.user).first()  # ここでログインユーザーに紐づくスタッフを取得
        
        Staff_id = self.kwargs.get('pk')  # URLのpkを取得

        # シフトスケジュールを取得（ログインユーザーに関連するもののみ）
        if Staff_id:
            print("--------------------------------------------------------")
            print("Staff_id:",Staff_id)
            shifts = ShiftSchedule.objects.filter(staff=Staff_id,
                                                  date__year=current_year, 
                                                  date__month=current_month).select_related('staff')
            print('shifts:',shifts)
        else:
            shifts = []  # スタッフが見つからなかった場合は空のリストを返す

        # 日付ごとにシフトをまとめた辞書を作成
        shift_dict = {}
        for shift in shifts:
            day = shift.date.day
            print("day:",day)
            if day not in shift_dict:
                shift_dict[day] = []
            shift_dict[day].append(shift)

        # 1週間ごとに日付を並べる
        days_in_month = list(range(1, 32))  # 1日から31日まで
        weeks_of_month = []

        # 月初めの日付が何曜日かによって開始日を調整
        # 1日の曜日に合わせて日付を並べる
        week = [None] * start_weekday  # 月の最初の日の前の空白を追加
        for day in days_in_month:
            if len(week) == 7:  # 1週間分埋まったら新しい週を作る
                weeks_of_month.append(week)
                week = []
            week.append(day)

        if len(week) > 0:  # 最後の週を追加（もし1週間が満杯でない場合）
            weeks_of_month.append(week)

        # コンテキストにデータを渡す
        context = {
            'shifts': shifts,
            'shift_dict': shift_dict,
            'current_month': current_month,
            'current_year': current_year,
            'weeks_of_month': weeks_of_month,
        }
        print("context:",context)

        return render(request, 'staff/shift_schedule.html', context)
