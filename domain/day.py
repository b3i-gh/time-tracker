from datetime import datetime


class Day:
    current_date = None
    is_today = False
    progress = 0
    time_spent = 0
    is_working_day = True
    
    def __init__(self, current_date, is_today, progress, time_spent):
        self.current_date = current_date
        if current_date == datetime.date.today():
            self.is_today = True
        else:
            self.is_today = False
        self.progress = progress
        self.time_spent = time_spent
        self.is_working_day = self.check_working_day(current_date)
    
    def check_working_day(self, current_date):
        if current_date.weekday() in [5, 6]:
            return False
