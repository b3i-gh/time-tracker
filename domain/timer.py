from datetime import datetime


class Timer:
    timer_id = None
    is_running = False
    date = None
    elapsed_time = None
    tracker_id = None

    def __init__(self, timer_id, tracker_id, date, elapsed_time):
        self.timer_id = timer_id
        self.tracker_id = tracker_id
        self.is_running = False
        self.date = date
        self.elapsed_time = elapsed_time
