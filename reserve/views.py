import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Seat, Schedule
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class AllSchedule(generic.ListView):
    template_name = 'reserve/all_schedule.html'
    model = Seat
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seats = Seat.objects.all()
        today = datetime.date.today()
        days = [today + datetime.timedelta(days=day) for day in range(7)]
        start_date = today
        end_date = days[-1]

        seats_days = [] #席・リストBのタプルを持つリストA
        for seat in seats:
            days_if_enable = [] #日付・予約可否のタプルを持つリストB
            for day in days:
                if_enable = not Schedule.objects.filter(seat=seat, date=day).exists() #予約可否を取得
                if not if_enable:
                    reserve_user = Schedule.objects.get(seat=seat, date=day).user #すでに予約が入っている場合、予約者を取得
                print(reserve_user)
                days_if_enable.append((day, if_enable, reserve_user)) #リストBに値をセット
            seats_days.append((seat, days_if_enable)) #リストAに値をセット
        
        context["seats"] = seats
        context["seat"] = seat
        context["days"] = days
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["seats_days"] = seats_days
        return context

class DoReserve(LoginRequiredMixin, generic.CreateView):
    template_name = 'reserve/do_reserve.html'
    model = Schedule
    fields = ()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.date(year=self.kwargs['year'], month=self.kwargs['month'], day=self.kwargs['day'])
        seat = get_object_or_404(Seat, pk=self.kwargs['pk'])
        
        context["seat"] = seat
        context["year"] = self.kwargs['year']
        context["month"] = self.kwargs['month']
        context["day"] = self.kwargs['day']
        return context
    
    def post(self, form, **kwargs):
        if self.request.method == "POST":
            seat = get_object_or_404(Seat, pk=self.kwargs['pk'])
            date = datetime.date(year=self.kwargs['year'], month=self.kwargs['month'], day=self.kwargs['day'])
            if Schedule.objects.filter(seat=seat, date=date).exists():
                messages.error(self.request, '入れ違いで予約がありました。')
            else:
                Schedule.objects.create(seat=seat, date=date, user=self.request.user)
            return redirect('reserve:all_schedule')

class MyPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reserve/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule_list'] = Schedule.objects.filter(user=self.request.user).order_by('user')
        return context