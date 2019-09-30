from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.staticfiles import finders 
from decimal import Decimal
import math
from users.models import CustomUser

from openpyxl import load_workbook
from preferences.models import Preferences
from preferences import preferences

# Create your models here.

class CoreAppSettings(Preferences):
    class Meta:
        verbose_name_plural = "core app settings"
    reimbursement_rate = models.FloatField(default=0.53)
    spreadsheet_email = models.CharField(max_length=255, default='jacksonfoster444@gmail.com')


class Entry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    entry_date = models.DateField('Date of entry')
    pub_date = models.DateField('Last modified')
    destination = models.CharField(max_length=500, blank=True)
    notes = models.CharField(max_length=500, blank=True)
    odo_start = models.FloatField(default=0)
    odo_end = models.FloatField(default=0, blank=True)
    pay_period_start = models.DateField('Week start')
    pay_period_end = models.DateField('Week end')
    draft = models.BooleanField(default=True)
    emailed = models.BooleanField(default=False)

    
    start_of_pay_period = 4 # friday
    end_of_pay_period = 3 # thursday


    

    @staticmethod
    def current_entries(user, date=timezone.now().date()):
        current_entries = Entry.objects.filter(
            user=user, 
            pub_date__gte=Entry().get_start_of_pay_period_date(date=date), # current pay period
            pub_date__lte=Entry().get_end_of_pay_period_date(date=date) # current pay period
            )
        return current_entries



    def miles_driven(self):
        return math.ceil(self.odo_end - self.odo_start)
    


    def amount_reimbursed(self, rate=None):
        if rate is None: # preferences gets screwy when running tests
            if preferences.CoreAppSettings.reimbursement_rate:
                rate = preferences.CoreAppSettings.reimbursement_rate
            else:
                rate = 0.53

        total = rate * self.miles_driven()
        return Decimal('{:.2f}'.format(round(total,2)))
    

    def get_start_of_pay_period_date(self, date=None):
        if date is None and self.pub_date: 
            date = self.pub_date
        else:
            date = timezone.now().date()

        one_week = timedelta(days=7)

        if date.weekday() >= self.start_of_pay_period: # friday, saturday and sunday
            return (date - timedelta(days=(date.weekday()-self.start_of_pay_period)))
        else:
            difference = self.start_of_pay_period - date.weekday()
            upcoming_friday = date + timedelta(days=difference)

            last_friday = upcoming_friday - one_week

            return last_friday


    def get_end_of_pay_period_date(self, date=None):
        if date is None and self.pub_date: 
            date = self.pub_date
        else:
            date = timezone.now().date()

        one_week = timedelta(days=7)

        if date.weekday() <= self.end_of_pay_period:
            difference = self.end_of_pay_period - date.weekday()
            upcoming_thursday = date + timedelta(days=difference)
            return upcoming_thursday
        else:
            difference = self.end_of_pay_period - date.weekday()
            last_thursday = date + timedelta(days=difference)

            next_thursday = last_thursday + one_week

            return next_thursday

