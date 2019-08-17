from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.staticfiles import finders 

from users.models import CustomUser

from openpyxl import load_workbook
from preferences.models import Preferences
from preferences import preferences

# Create your models here.

class CoreAppSettings(Preferences):
    class Meta:
        verbose_name_plural = "core app settings"
    reimbursement_rate = models.FloatField(null=True, blank=True)
    spreadsheet_email = models.CharField(max_length=255, blank=True, null=True)


class Entry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    entry_date = models.DateField('Date of entry')
    destination = models.CharField(max_length=500)
    notes = models.CharField(max_length=500)
    odo_start = models.IntegerField()
    odo_end = models.IntegerField()
    pay_period_start = models.DateField('Week start')
    pay_period_end = models.DateField('Week end')

    
    start_of_pay_period = 4 # friday
    end_of_pay_period = 3 # thursday


    

    @staticmethod
    def current_entries(user, date=datetime.today()):
        current_entries = Entry.objects.filter(user=user, pay_period_start=Entry().get_start_of_pay_period_date(date=date))
        return current_entries



    def miles_driven(self):
        return self.odo_end - self.odo_start
    


    def amount_reimbursed(self):
        rate = preferences.CoreAppSettings.reimbursement_rate #pylint: disable=no-member
        return round(rate * self.miles_driven(), 2)
    

    def get_start_of_pay_period_date(self, date):
        one_week = timedelta(days=7)

        if date.weekday() >= self.start_of_pay_period: # friday, saturday and sunday
            return (date - timedelta(days=(date.weekday()-self.start_of_pay_period)))
        else:
            difference = self.start_of_pay_period - date.weekday()
            upcoming_friday = date + timedelta(days=difference)

            last_friday = upcoming_friday - one_week

            return last_friday


    def get_end_of_pay_period_date(self, date):
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

class TestSpreadsheet():
    def __init__(self):
        from datetime import datetime, timedelta
        from users.models import CustomUser
        from core.utils import Spreadsheet
        from core.models import Entry
        day = datetime.today() - timedelta(days=7)
        u = CustomUser.objects.last()
        s = Spreadsheet(u)
        entries = s.entries_for_pay_period(date=day)
        self.sheet = s.write_to_spreadsheet(entries)
    
    def run(self):
        return self.sheet
