from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps
from preferences import preferences
from decimal import Decimal

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    contractor = models.CharField(max_length=500, default='MYZ')

    def __str__(self):
        return "{0}, {1} | {2}".format(self.last_name, self.first_name, self.username)
    
    def total_miles_driven(self):
        total = 0
        Entry = apps.get_model('core.Entry') # must use a lazy import, otherwise you'll get a circular import
        entries = Entry.objects.filter(user=self, draft=False)

        for entry in entries:
            miles_driven = entry.odo_end - entry.odo_start
            total += miles_driven

        return total
    
    def total_amount_reimbursed(self):
        total = 0
        Entry = apps.get_model('core.Entry') # must use a lazy import, otherwise you'll get a circular import
        entries = Entry.objects.filter(user=self, draft=False)

        for entry in entries:
            amount = preferences.CoreAppSettings.reimbursement_rate * entry.miles_driven() #pylint: disable=no-member
            total += amount

        return Decimal('{:.2f}'.format(round(total,2)))
