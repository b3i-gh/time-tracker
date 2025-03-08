from datetime import datetime
import tkinter as tk

try:
    from repository.database_manager import DatabaseManager
    from repository.tracker_repository import Tracker_Repository
    from repository.timer_repository import Timer_Repository
    from service.tracker_service import Tracker_Service
except ImportError as e:
    raise ImportError(f"Error importing required classes: {e}")

class TimeTrackerApp:
    trackers = []

    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        trackers = []

        dbManager = DatabaseManager(True)
        tracker_repo = Tracker_Repository(dbManager)
        timer_repo = Timer_Repository(dbManager)

        # loads the trackers
        trackers_data = tracker_repo.get_trackers()

        # initializes the trackers
        for tracker in trackers_data:
            tracker.timer = timer_repo.get_timer_for_tracker_and_day(tracker.tracker_id, datetime.today())
            trackers.append(tracker)
            tracker_service = Tracker_Service(tracker, tracker_repo, timer_repo, self.root)     
            tracker_service.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()