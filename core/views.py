from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Entry
from .forms import EntryForm
from preferences import preferences
from core.utils import Spreadsheet

# Create your views here.
def index(request):
    current_entry_list = Entry.current_entries(request.user)
    return render(request, 'core/index.html', {'current_entry_list': current_entry_list})



def list(request):
    entries = Entry.objects.filter(user=request.user)
    return render(request, 'core/list.html', {'entries': entries})
    


def new(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('core:index')
    else:
        form = EntryForm()
        return render(request, 'core/new.html', {'form': form})



def detail(request, id):
    entry = Entry.objects.get(id=id)
    return render(request, 'core/detail.html', {'entry': entry})
 


def edit(request, id):
    entry = Entry.objects.get(id=id)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)

        if form.is_valid():
            form.save(request)
            return redirect('core:index')
        else:
                return render(request, 'core/edit.html', {'form': form, 'entry': entry })

    else:
        form = EntryForm(instance=entry)
        return render(request, 'core/edit.html', {'form': form, 'entry': entry})



def delete(request, id):
    Entry.objects.get(id=id).delete()
    return redirect('core:index')

def view_sheet(request, id):
    entry = Entry.objects.get(id=id)
    sheet = Spreadsheet(request.user, entry).as_dict()
    keys = []
    for key in sheet['entries'][0].keys():
            keys.append(key.title().replace("_", " "))
    return render(request, 'core/sheet.html', {'keys': keys,'sheet': sheet, 'pay_period_start': entry.pay_period_start, 'pay_period_end': entry.pay_period_end})
    