from django.db import models
from datetime import date
from django.utils import timezone

class Seat(models.Model):
    name = models.CharField('席名', max_length=255)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    date = models.DateField('予約日')
    seat = models.ForeignKey('Seat', verbose_name='席', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)   # timezone is defined on setting.py

    def __str__(self):
        return f'席{self.seat} {date}'