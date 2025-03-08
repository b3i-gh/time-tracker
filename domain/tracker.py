class Tracker:
    tracker_id = None
    tracker_name = None
    expected_duration = None
    timer = None

    # GUI
    timer_label = None
    start_button = None
    stop_button = None

    def __init__(self, tracker_id, tracker_name, expected_duration):
        self.tracker_id = tracker_id
        self.tracker_name = tracker_name
        self.expected_duration = expected_duration        