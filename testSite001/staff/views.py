# staff/views.py
from django.shortcuts import render, get_object_or_404, redirect
from main.models import *
from .forms import StaffForm

# スタッフ一覧ページ
def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'staff/staff_list.html', {'staff': staff})

# スタッフ詳細ページ
def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    return render(request, 'staff/staff_detail.html', {'staff': staff})

# スタッフ追加ページ
def staff_add(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff:staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff/staff_form.html', {'form': form})
