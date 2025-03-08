from datetime import datetime
import sqlite3
from domain.timer import Timer

class Timer_Repository:
    db = None
    
    def __init__(self, dbManager):
        self.db = dbManager.db
    
    def save_timer(self, timer, selected_date = datetime.today()):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        date = selected_date.strftime("%Y-%m-%d")
        if timer.timer_id:
            cursor.execute("UPDATE timers SET tracker_id = ?, date = ?, elapsed_time = ? WHERE timer_id = ?", (timer.tracker_id, date, timer.elapsed_time, timer.timer_id))
        else:
            cursor.execute("INSERT INTO timers (tracker_id, date, elapsed_time) VALUES (?, ?, ?)", (timer.tracker_id, date, timer.elapsed_time))
            timer.timer_id = cursor.lastrowid
        connection.commit()
        connection.close()

    def get_timer(self, timer_id):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM timers where timer_id = ?", (timer_id))
        timer = cursor.fetchone()
        connection.close()
        return timer

    def get_timer_for_tracker_and_day(self, tracker_id, date = datetime.today()):
        date_filter = date.strftime("%Y-%m-%d")
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM timers WHERE tracker_id = ? AND date = ?", (tracker_id, date_filter))        
        row = cursor.fetchone()
        timer = Timer(*row) if row else Timer(None, tracker_id, date_filter, 0)
        connection.close()
        return timer
    
    def get_monthly_timers_for_tracker(self, tracker_id, month, year):
        month_filter = year + "-" + month + "%"
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM timers WHERE tracker_id = ? AND date LIKE ? ORDER BY date ASC", (tracker_id, month_filter))
        recap = {}
        for r in cursor.fetchall():
            day = r[2][-2:]
            recap[day] = r
        connection.close()
        return recap