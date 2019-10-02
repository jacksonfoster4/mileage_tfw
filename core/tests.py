from django.test import TestCase
from .models import Entry, CoreAppSettings
from .utils import Spreadsheet
from datetime import datetime, date, timedelta
from users.models import CustomUser
from preferences import preferences
from decimal import Decimal
from io import BytesIO

# Create your tests here.
    
class EntryTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.reimbursement_rate = 0.53
        self.user = CustomUser.objects.create(first_name = "Mr.", last_name= "Present", username="Current User")
        self.entries = [{"user":self.user, "entry_date": datetime.today(), "pub_date":datetime.today(), "notes": "Test Entry", "destination": "Job 1", "odo_start":123, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}, 
        {"user":self.user, "entry_date": datetime.today(), "pub_date":datetime.today(), "notes": "Test Entry", "destination": "Job 2", "odo_start":128, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}, 
        {"user":self.user, "entry_date": datetime.today(), "pub_date":datetime.today(), "notes": "Test Entry", "destination": "Job 3", "odo_start":163, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}]
        
        [ Entry.objects.create(**e) for e in self.entries ]
        self.entries = Entry.objects.filter(user_id=self.user.id)
    #current_entries(...)
        # does it return [] for past entries?
        # does it return [] for future entries
        # does it return QuerySet for current entries?
    def test_current_entries_past(self):
        user = CustomUser.objects.create(first_name = "Mr.", last_name= "Past", username="Past User")
        past = [{"user":user, "entry_date": datetime.today()-timedelta(days=12), "pub_date":datetime.today()-timedelta(days=12), "destination": "Job 1", "odo_start":123, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()-timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()-timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()-timedelta(days=12), "pub_date":datetime.today()-timedelta(days=12), "destination": "Job 2", "odo_start":128, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()-timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()-timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()-timedelta(days=12), "pub_date":datetime.today()-timedelta(days=12), "destination": "Job 3", "odo_start":163, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()-timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()-timedelta(days=12))}]
        
        [ Entry.objects.create(**e) for e in past ]

        self.assertEquals(len(Entry.current_entries(user)), 0) 

    def test_current_entries_current(self):
        self.assertEquals(len(Entry.current_entries(self.user)), 3) 


    def test_current_entries_future(self):
        user = CustomUser.objects.create(first_name = "Mr.", last_name= "Future", username="Future User")
        future = [{"user":user, "entry_date": datetime.today()+timedelta(days=12), "pub_date":datetime.today()+timedelta(days=12), "destination": "Job 1", "odo_start":123, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()+timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()+timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()+timedelta(days=12), "pub_date":datetime.today()+timedelta(days=12), "destination": "Job 2", "odo_start":128, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()+timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()+timedelta(days=12))}, 
        {"user":user, "entry_date": datetime.today()+timedelta(days=12), "pub_date":datetime.today()+timedelta(days=12), "destination": "Job 3", "odo_start":163, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()+timedelta(days=12)),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today()+timedelta(days=12))}]
        
        [ Entry.objects.create(**e) for e in future ]
        
        # is `current_entries` empty?
        self.assertEquals(len(Entry.current_entries(user)), 0) 
        
    def test_miles_driven(self):
        for entry in self.entries:
            self.assertEquals(entry.miles_driven(), entry.odo_end - entry.odo_start)
        
    def test_amount_reimbursed(self):
        for entry in self.entries:
            self.assertEquals(entry.amount_reimbursed(rate=self.reimbursement_rate), Decimal('{:.2f}'.format(round(entry.miles_driven() * self.reimbursement_rate, 2))))
    
    def test_get_start_of_pay_period_date(self):
        pub_date = date(2019, 9, 9)
        pay_period_start = date(2019, 9, 6)
        self.assertEquals(Entry().get_start_of_pay_period_date(date=pub_date), pay_period_start)
            
    def test_get_end_of_pay_period_date(self):
        pub_date = date(2019, 9, 9)
        pay_period_end = date(2019, 9, 12)
        self.assertEquals(Entry().get_end_of_pay_period_date(date=pub_date), pay_period_end)

class SpreadsheetTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.reimbursement_rate = 0.53
        self.user = CustomUser.objects.create(first_name = "Mr.", last_name= "Present", username="Current User")
        self.entries = [{"user":self.user, "entry_date": datetime.today(), "pub_date":datetime.today(), "notes": "Test Entry", "destination": "Job 1", "odo_start":123, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}, 
        {"user":self.user, "entry_date": datetime.today(), "pub_date":datetime.today(), "notes": "Test Entry", "destination": "Job 2", "odo_start":128, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}, 
        {"user":self.user, "entry_date": datetime.today(), "pub_date":datetime.today(), "notes": "Test Entry", "destination": "Job 3", "odo_start":163, "odo_end": 456, "pay_period_start": Entry().get_start_of_pay_period_date(datetime.today()),"pay_period_end": Entry().get_end_of_pay_period_date(datetime.today())}]
        
        [ Entry.objects.create(**e) for e in self.entries ]

        self.entries = Entry.objects.filter(user_id=self.user.id)
        self.workbook = Spreadsheet(self.user, self.entries)
        self.sheet = self.workbook.write_to_spreadsheet()

    def test_write_to_spreadsheet(self):
        miles_driven = 0
        total_reimbursement = 0
        for i, entry in enumerate(self.entries):
            expected_values = {
                'B3': "{} {}".format(self.user.first_name, self.user.last_name),
                'E3': "${}".format(self.reimbursement_rate),
                "A{}".format(i+8): entry.pub_date.strftime("%m-%d-%Y"),
                "B{}".format(i+8): entry.destination,
                "C{}".format(i+8): entry.notes,
                "D{}".format(i+8): entry.odo_start,
                "E{}".format(i+8): entry.odo_end,
                "F{}".format(i+8): entry.miles_driven(),
                "G{}".format(i+8): "${}".format(round(entry.miles_driven() * self.reimbursement_rate, 2))
            }
            miles_driven += entry.miles_driven()
            total_reimbursement +=  round(entry.miles_driven() * self.reimbursement_rate, 2)

            for cell, expected_value in expected_values.items():
                self.assertEquals(self.sheet[cell].value, expected_value)

        self.assertEquals(self.sheet['E4'].value, miles_driven)
        self.assertEquals(self.sheet['E5'].value, "${}".format(total_reimbursement))

    # as_dict(...)
        # check each key to ensure it matches entries and user
    def test_save_to_binary_stream(self):
        self.assertIsInstance(self.workbook.save_as_binary_stream(), BytesIO)

    

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



