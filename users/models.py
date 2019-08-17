from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return "{0}, {1} | {2}".format(self.last_name, self.first_name, self.username)
    
    def total_miles_driven(self):
        total = 0
        Entry = apps.get_model('core.Entry') # must use a lazy import, otherwise you'll get a circular import
        entries = Entry.objects.filter(user=self)

        for entry in entries:
            miles_driven = entry.odo_end - entry.odo_start
            total += miles_driven

        return total
    
    def total_amount_reimbursed(self):
        total = 0
        Entry = apps.get_model('core.Entry') # must use a lazy import, otherwise you'll get a circular import
        entries = Entry.objects.filter(user=self)

        for entry in entries:
            amount = entry.reimbursement_rate * entry.miles_driven()
            total += amount

        return total
