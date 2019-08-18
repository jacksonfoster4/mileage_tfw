from preferences import preferences
from .models import Entry
from openpyxl import load_workbook
from django.contrib.staticfiles import finders 
from django.conf import settings
from datetime import datetime
from io import BytesIO


class Spreadsheet():
    def __init__(self, user, entry=None):
        self.email = preferences.CoreAppSettings.spreadsheet_email #pylint: disable=no-member
        self.user = user
        if entry is not None:
            self.entries = self.entries_for_pay_period(entry.pub_date)
        else:
            self.entries = self.entries_for_pay_period(datetime.today())
        self.offset = 8 # where the entries begin

        self.cell = lambda column, row: "{}{}".format(self.columns[column],row)
        
        self.cells = {
            'total_mileage': 'F4',
            'total_reimbursement': 'F5',
            'employee_name': 'B3'
        }

        self.columns = {
            'date': 'A',
            'destination': 'B',
            'notes': 'C',
            'odo_start': 'D',
            'odo_end': 'E',
            'mileage': 'F',
            'reimbursement': 'G'
        }

        self.total_miles = 0
        self.total_reimbursement = 0

        self.load_spreadsheet_template()

    
    def load_spreadsheet_template(self):
        name = finders.find("core/{}".format(settings.SPREADSHEET_NAME))
        self.wb = load_workbook(filename=name)
    


    def entries_for_pay_period(self, date):
        entries = Entry.current_entries(self.user, date)
        return entries



    def as_dict(self):
        ws = self.wb.active
        total_miles, total_reimbursement = 0, 0

        final = {'entries': []}

        for entry in self.entries:
            entry_dict = {}
            total_miles += entry.miles_driven()
            total_reimbursement += entry.amount_reimbursed()

            entry_dict['date'] = entry.entry_date.strftime("%m-%d-%Y")
            entry_dict['destination'] = entry.destination
            entry_dict['notes'] = entry.notes
            entry_dict['odometer_start'] = entry.odo_start
            entry_dict['odometer_end'] = entry.odo_end
            entry_dict['mileage'] = entry.miles_driven()
            entry_dict['reimbursement'] = entry.amount_reimbursed()

            final['entries'].append(entry_dict)
        

        final['total_mileage'] = self.total_miles
        final['total_reimbursement'] = self.total_reimbursement
        final['employee_name'] = "{} {}".format(self.user.first_name, self.user.last_name)

        return final



    def write_to_spreadsheet(self):
        ws = self.wb.active
        total_miles, total_reimbursement = 0, 0

        for i, entry in enumerate(self.entries):
            row = i + self.offset

            self.total_miles += entry.miles_driven()
            self.total_reimbursement += entry.amount_reimbursed()

            ws[self.cell('date',row)] = entry.entry_date.strftime("%m-%d-%Y")
            ws[self.cell('destination',row)] = entry.destination
            ws[self.cell('notes',row)] = entry.notes
            ws[self.cell('odometer_start',row)] = entry.odo_start
            ws[self.cell('odometer_end',row)] = entry.odo_end
            ws[self.cell('mileage',row)] = entry.miles_driven()
            ws[self.cell('reimbursement',row)] = entry.amount_reimbursed()

        ws[self.cells['total_mileage']] = total_miles
        ws[self.cells['total_reimbursement']] = total_reimbursement
        ws[self.cells['employee_name']] = "{} {}".format(self.user.first_name, self.user.last_name)

        end_of_entries = len(self.entries) + self.offset
        ws[self.cell('mileage', end_of_entries)] = total_miles
        ws[self.cell('reimbursement', end_of_entries)] = "${}".format(total_reimbursement)


        self.wb.active = ws
        return self.wb.active



    def save_as_binary_stream(self):
        stream = BytesIO()
        self.wb.save(stream)
        return stream

