from __future__ import absolute_import
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mileage_logger.settings')
django.setup() # apps need to be installed before models are imported

from celery import Celery
from celery.schedules import crontab
from users.models import CustomUser
from core.models import Entry
from core.utils import Spreadsheet
from datetime import date, timedelta


app = Celery('mileage_logger')
app.config_from_object('django.conf:settings')
app.conf.timezone = 'US/Pacific'

app.conf.beat_schedule = {
    # Executes every Thursday at 6:30

    # there is a separate cronjob that runs every thursday at midnight.
    # this is to purge caches. if you change this schedule, be sure to change the cronjob.
    'send-sheets-every-thursday-afternoon': {
        'task': 'send_spreadsheets',
        'schedule': crontab(hour=18, minute=30, day_of_week=4),
    },
}

@app.task(name="send_spreadsheets")
def send_spreadsheets():
    users = CustomUser.objects.all()
    for user in users:
        filter_current_entries = lambda entry: entry.get_end_of_pay_period_date() == date.today() and entry.draft==False
        entries = list( filter( filter_current_entries, Entry.objects.filter(user=user) ) )
        if entries:
            Spreadsheet(user, entries).send_spreadsheet()

@app.task(name="test_send_spreadsheets")
def test_send_spreadsheets():
    users = CustomUser.objects.all()
    for user in users:
        filter_current_entries = lambda entry: entry.get_end_of_pay_period_date() == date.today()+timedelta(days=2) and entry.draft==False
        entries = list( filter( filter_current_entries, Entry.objects.filter(user=user) ) )
        if entries:
            Spreadsheet(user, entries).send_spreadsheet()
""" need to initialize beat scheduler 
        celery -A mileage_logger beat 
    and then initialize the worker process
        celery -A mileage_logger worker -l INFO
    from command line...
    from celery import Celery
    celery = Celery()
    celery.config_from_object('django.conf:settings')
    celery.send_task('send_spreadsheets')

"""