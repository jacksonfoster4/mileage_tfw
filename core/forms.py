from django.forms import ModelForm
from .models import Entry
from preferences import preferences
from django.utils import timezone
from django import forms

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_date', 'destination', 'notes', 'odo_start', 'odo_end']
        widgets = {
            'entry_date': forms.DateTimeInput(attrs={'placeholder': 'M/D/YYYY'}, format="%m/%d/%y"),
        }
    
    def save(self, request, commit=True):
        obj = super().save(commit=False)
        obj.user = request.user
        obj.pub_date = timezone.now().date()
        obj.pay_period_start = obj.get_start_of_pay_period_date()
        obj.pay_period_end = obj.get_end_of_pay_period_date()
        
        if 'save' in request.POST:
            obj.draft = False
        elif 'save_as_draft' in request.POST:
            obj.draft = True

        if commit:
            obj.save()
        else:
            return obj
        