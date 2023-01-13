import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Seat, Schedule
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse

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

        calendar = {}
#        calendar = [[True for i in range(len(days))] for j in range(seats.count())]
        for k, seat in enumerate(seats):
            for l, day in enumerate(days):
                if Schedule.objects.filter(seat=seat, date=day).exists():
                    #print("999")
                    calendar[k][l] = False
                    #print(k, l, calendar[k][l])
                else:
                    calendar[k][l] = True
                #print(l, k)
            #print(k)
        print(calendar)

        context["seats"] = seats
        context["seat"] = seat
        context["days"] = days
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["calendar"] = calendar
        return context

class DoReserve(generic.CreateView):
    template_name = 'reserve/do_reserve.html'
    model = Schedule
    fields = ()
    
    def get_context_data(self, **kwargs):
        #print(self.request.method + "1")
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
                Schedule.objects.create(seat=seat, date=date)
                #print(self.request.method + "2")
            return redirect('reserve:all_schedule')