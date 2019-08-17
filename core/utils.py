from preferences import preferences
from .models import Entry
from openpyxl import load_workbook
from django.contrib.staticfiles import finders 
from django.conf import settings
from datetime import datetime



class Spreadsheet():
    def __init__(self, user):
        self.email = preferences.CoreAppSettings.spreadsheet_email #pylint: disable=no-member
        self.user = user
        self.load_spreadsheet_template()
    
    def entries_for_pay_period(self, date=datetime.today()):
        entries = Entry.current_entries(self.user, date)
        return entries
    
    def load_spreadsheet_template(self):
        name = finders.find("core/{}".format(settings.SPREADSHEET_NAME))
        wb = load_workbook(filename=name)
        self.ws = wb.copy_worksheet(wb.active)
    

    def write_to_spreadsheet(self, entries):
        ws = self.ws
        offset = 8 # where the entries begin

        cell = lambda column, row: "{}{}".format(columns[column],row)
        
        cells = {
            'total_mileage': 'F4',
            'total_reimbursement': 'F5',
            'employee_name': 'B3'
        }
        columns = {
            'date': 'A',
            'destination': 'B',
            'notes': 'C',
            'odo_start': 'D',
            'odo_end': 'E',
            'mileage': 'F',
            'reimbursement': 'G'
        }

        total_miles = 0
        total_reimbursement = 0

        for i, entry in enumerate(entries):
            row = i + offset

            total_miles += entry.miles_driven()
            total_reimbursement += entry.amount_reimbursed()

            ws[cell('date',row)] = entry.entry_date
            ws[cell('destination',row)] = entry.destination
            ws[cell('notes',row)] = entry.notes
            ws[cell('odo_start',row)] = entry.odo_start
            ws[cell('odo_end',row)] = entry.odo_end
            ws[cell('mileage',row)] = entry.miles_driven()
            ws[cell('reimbursement',row)] = entry.amount_reimbursed()

        ws[cells['total_mileage']] = total_miles
        ws[cells['total_reimbursement']] = total_reimbursement
        ws[cells['employee_name']] = "{} {}".format(self.user.first_name, self.user.last_name)

        end_of_entries = len(entries) + offset
        ws[cell('mileage', end_of_entries)] = total_miles
        ws[cell('reimbursement', end_of_entries)] = "${}".format(total_reimbursement)

        return ws
