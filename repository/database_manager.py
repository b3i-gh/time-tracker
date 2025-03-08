import sqlite3


class DatabaseManager:
    db = None
    
    def __init__(self, is_dev):
        if is_dev:
            self.db = 'time-tracker-dev-v2.db'
            connection = sqlite3.connect(self.db)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS trackers (tracker_id INTEGER PRIMARY KEY, tracker_name TEXT, expected_duration INTEGER)")
            cursor.execute("CREATE TABLE IF NOT EXISTS timers (timer_id INTEGER PRIMARY KEY, tracker_id TEXT NOT NULL, date TEXT, elapsed_time INTEGER)")
            connection.close()
        else:
            self.db = 'time-tracker.db'