from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'reserve'
urlpatterns = [
    path('', views.AllSchedule.as_view(), name='all_schedule'),
    path('<int:pk>/<int:year>/<int:month>/<int:day>/', views.DoReserve.as_view(), name='do_reserve'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mypage/', views.MyPage.as_view(), name='mypage'),
]