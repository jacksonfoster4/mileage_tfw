from django.test import TestCase
from .models import Entry
from .utils import Spreadsheet
from datetime import datetime, timedelta
from users.models import CustomUser
# Create your tests here.
class EntryTestCase(TestCase):


#    current_entries(...)
        # does it return [] for past entries?
        # does it return [] for future entries
        # does it return QuerySet for current entries?
    def test_current_entries_past(self):
        user = CustomUser.objects.create(first_name = "Mr.", last_name= "Past", username="Past User")
        past = [{"user":user, "entry_date": datetime.today()-timedelta(days=12), "pub_date":datetime.today()-timedelta(days=12), "destination": "Job 1", "odo_start":123, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()-timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()-timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()-timedelta(days=12), "pub_date":datetime.today()-timedelta(days=12), "destination": "Job 2", "odo_start":128, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()-timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()-timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()-timedelta(days=12), "pub_date":datetime.today()-timedelta(days=12), "destination": "Job 3", "odo_start":163, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()-timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()-timedelta(days=12))}]
        past_entries = [ Entry.objects.create(**e) for e in past ]

        self.assertEquals(len(Entry.current_entries(user)), 0) 




    def test_current_entries_current(self):
        user = CustomUser.objects.create(first_name = "Mr.", last_name= "Present", username="Current User")
        current = [{"user":user, "entry_date": datetime.today(), "pub_date":datetime.today(), "destination": "Job 1", "odo_start":123, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}, 
        {"user":user, "entry_date": datetime.today(), "pub_date":datetime.today(), "destination": "Job 2", "odo_start":128, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}, 
        {"user":user, "entry_date": datetime.today(), "pub_date":datetime.today(), "destination": "Job 3", "odo_start":163, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}]
        current_entries = [ Entry.objects.create(**e) for e in current ]

        self.assertEquals(len(Entry.current_entries(user)), 3) 



    def test_current_entries_future(self):
        user = CustomUser.objects.create(first_name = "Mr.", last_name= "Future", username="Future User")
        future = [{"user":user, "entry_date": datetime.today()+timedelta(days=12), "pub_date":datetime.today()+timedelta(days=12), "destination": "Job 1", "odo_start":123, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()+timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()+timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()+timedelta(days=12), "pub_date":datetime.today()+timedelta(days=12), "destination": "Job 2", "odo_start":128, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()+timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()+timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()+timedelta(days=12), "pub_date":datetime.today()+timedelta(days=12), "destination": "Job 3", "odo_start":163, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()+timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()+timedelta(days=12))}]
        future_entries = [ Entry.objects.create(**e) for e in future ]
        
        # is `current_entries` empty?
        self.assertEquals(len(Entry.current_entries(user)), 0) 
        


    
    def test_miles_driven(self):
        pass
    # miles_driven(...) 
        # does miles driven return a positive integer?
        # how does it handle blank odometer readings?
        # how does it handle negative odometer readings?
    
    # amount_reimbursed(...)
        # does it return the proper amount rounded to two decimal places
    
    # get_start_of_pay_period_date(...)
        # given no date, does the function return the start of the pay period of `self`?
        # given a date, does the function return the correct start of the pay period?
        # can it handle an invalid date?

    # get_end_of_pay_period_date(...)
        # given no date, does the function return the end of the pay period of `self`?
        # given a date, does the function return the correct end of the pay period?
        # can it handle an invalid date?
    pass

class SpreadsheetTestCase(TestCase):
    # create a list of entries
    # create user

    # write_to_spreadsheet(...)
        # check each cell to ensure it matches entries and user

    # as_dict(...)
        # check each key to ensure it matches entries and user

    # save_as_binary_stream(...)
        # does it return a binary stream

    pass

class CoreIndexViewTests(TestCase):
    # if i navigate to 'app/' does it render 'core/index.html'?

    # create series of past entries
    # create series of future entries
    # create series of current entries
    # create series of drafts

    # does current_entry_list return only current entries?
    # does drafts return only drafts?
    # is miles_driven_this_period(...) accurate?
    # is reimbursement_this_period(...) accurate?
    pass

class CoreListViewTests(TestCase):
    # if i navigate to 'app/list' does it render 'core/list.html'?

    # create user
    # get list of entries from user
    # does list_entries(...) return the proper entries?
    pass

class CoreNewViewTests(TestCase):
    # if i navigate to 'app/new' does it render 'core/new.html'?

    # create dict containing all fields and values for entry
    # if i post a proper object to 'core/new', does it create a proper object?
    # if i post an incorrect object to 'core/new', does it create an incorrect object? how is the error handled?
    pass

class CoreDetailViewTests(TestCase):
    # if i navigate to 'app/detail' does it render 'core/detail.html'?
    # create object
    # if i pass a non existent id, does it redirect?
    # if pass an id for an object, does the view match the object?
    pass

class CoreEditViewTests(TestCase):
    # if i navigate to 'app/edit' does it render 'core/edit.html'?

    # create object

    # if published in the past, does the warning show up?
    # if i post a proper object to 'core/edit', does it update the object?
    # if i post an incorrect object to 'core/edit', does it update the object? how does it handle it?
    pass

class CoreDeleteViewTests(TestCase):
    # create object

    # if i post to 'app/delete' does it delete the object?
    # if i post an invalid id, how is it handled?
    pass

class CoreViewSheetTests(TestCase):
    # if i navigate to 'app/sheet' does it render 'core/sheet.html'?

    # create series of entries
    # pick one entry

    # do the entries in view_sheet(...) all belong in the same period?
    # what if there is no entry?
    pass



