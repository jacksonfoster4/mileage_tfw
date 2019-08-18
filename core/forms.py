from django.forms import ModelForm
from .models import Entry
from preferences import preferences
from datetime import datetime

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_date', 'destination', 'notes', 'odo_start', 'odo_end']
    
    def save(self, request, commit=True):
        obj = super().save(commit=False)
        obj.user = request.user
        obj.pay_period_start = obj.get_start_of_pay_period_date()
        obj.pay_period_end = obj.get_end_of_pay_period_date()
        obj.pub_date = datetime.today()
        if commit:
            obj.save()
        else:
            return obj
        