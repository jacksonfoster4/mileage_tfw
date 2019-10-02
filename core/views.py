from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Entry
from .forms import EntryForm
from preferences import preferences
from core.utils import Spreadsheet
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from decimal import Decimal

@login_required
def index(request):
    entries = Entry.current_entries(request.user)
    all_entries = list(Entry.objects.filter(user=request.user, draft=False))

    drafts = list(filter(lambda x: x.draft == True, entries))
    drafts.reverse()
    current_drafts = list(zip(drafts, list(map(lambda x: EntryForm(instance=x), drafts))))
    
    current_entry_list = list(filter(lambda x: x.draft == False, entries))
    current_entry_list.reverse()
    current_entries = list(zip(current_entry_list, list(map(lambda x: EntryForm(instance=x), current_entry_list))))
    
    miles_driven_this_period = sum(map(lambda x: x.miles_driven(), current_entry_list))
    reimbursement_this_period = Decimal('{:.2f}'.format(round(miles_driven_this_period * preferences.CoreAppSettings.reimbursement_rate, 2))) # pylint: disable=no-member
    return render(request, 'core/index.html', {'current_entries': current_entries,
                                                'current_drafts': current_drafts, 
                                                'miles_driven_this_period': miles_driven_this_period, 
                                                'reimbursement_this_period': reimbursement_this_period,
                                                'form': EntryForm(initial={'odo_start': None, 'odo_end': None}),
                                                'total_reimbursement': sum(map(lambda x: x.amount_reimbursed(), all_entries)),
                                                'total_miles_driven': sum(map(lambda x: x.miles_driven(), all_entries)),
                                                'start_of_this_pay_period': Entry().get_start_of_pay_period_date().strftime("%b %d %Y"),
                                                'end_of_this_pay_period': Entry().get_end_of_pay_period_date().strftime("%b %d %Y")
                                                })


@login_required
def list_entries(request):
    entries = list(Entry.objects.filter(user=request.user, draft=False))
    entries.reverse()
    dict = { }
    pay_periods = []
    for entry in entries:
        date = entry.pay_period_start
        if date in dict:
                dict[date].append(entry)
        else:
                dict[date] = [entry]
    for d in dict.keys():
        pay_periods.append({'start_date': d, 'end_date': d + timedelta(days=6), 'entries': dict[d]})
    for period in pay_periods:
        forms = []
        for entry in period['entries']:
            forms.append(EntryForm(instance=entry))
        period['entries'] = zip(period['entries'], forms)
    return render(request, 'core/list.html', {'pay_periods': pay_periods})
    

@login_required
def new(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('core:index')
        else:
            return render(request, 'core/new.html', {'form': form})
    else:
        form = EntryForm()
        return render(request, 'core/new.html', {'form': form})


@login_required
def detail(request, id):
    entry = Entry.objects.get(id=id)
    return render(request, 'core/detail.html', {'entry': entry})
 

@login_required
def edit(request, id):
    entry = Entry.objects.get(id=id)
    if not entry:
        redirect('core:app')
    warning = None
    if entry.pub_date < entry.get_start_of_pay_period_date(date=timezone.now().date()):
        warning = "This entry will be moved to the current pay period. Are you sure you want to continue?"

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save(request)
            return redirect('core:index')
        else:
            return render(request, 'core/edit.html', {'form': form, 'entry': entry, 'warning': warning })

    else:
        form = EntryForm(instance=entry)
        return render(request, 'core/edit.html', {'form': form, 'entry': entry, 'warning': warning})


@login_required
def delete(request, id):
    Entry.objects.filter(id=id).delete()
    return redirect('core:index')

@login_required
def view_sheet(request, id):
    entry = Entry.objects.get(id=id)
    entries = Entry.current_entries(request.user, entry.pub_date)
    sheet = Spreadsheet(request.user, entries).as_dict()
    keys = []
    for key in sheet['entries'][0].keys():
            keys.append(key.title().replace("_", " "))
    print(sheet)
    return render(request, 'core/sheet.html', {'keys': keys,'sheet': sheet, 'pay_period_start': entry.pay_period_start, 'pay_period_end': entry.pay_period_end})
    