from django.urls import path
from . import views

app_name = 'reserve'
urlpatterns = [
    #path('', views.SeatList.as_view(), name='seat_list'),
    path('', views.AllSchedule.as_view(), name='all_schedule'),
    #path('<int:pk>', views.Calendar.as_view(), name='calendar'),
    path('<int:pk>/<int:year>/<int:month>/<int:day>/', views.DoReserve.as_view(), name='do_reserve'),
]