import sqlite3
from domain.tracker import Tracker

class Tracker_Repository:
    db = None
    
    def __init__(self, dbManager):
        self.db = dbManager.db
    
    def get_tracker(self, tracker_id):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM trackers WHERE tracker_id = ?", (tracker_id,))       
        tracker = Tracker(cursor.fetchone())
        connection.close()
        return tracker

    def get_trackers(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM trackers")
        trackers = cursor.fetchall()
        result = []
        for r in trackers:
            tracker = Tracker(*r)
            result.append(tracker)
        connection.close()
        return result