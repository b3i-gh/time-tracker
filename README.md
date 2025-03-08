# Time Tracker

## Description

Time Tracker is a simple application to help you keep track of the time you spend on various tasks and projects;
tkinter is used for the GUI and sqlite3 for the data persistence.
You can customize the tracked tasks by modifying timer_categories and timer_thresholds (if you need to track more than 3 tasks, you should also customize the GUI).

**Usage: since v2.0.0 `DatabaseManager` will by default connect to a testing db (`time-tracker-dev-v2.db`); to work with a _production environment db_ (`time-tracker.db`) change the dbManager instantiation inside `main.py` as follows:**

`dbManager = DatabaseManager(False)`

## v1.0.0

- keeps track of 3 default categories;
- saves the timers of each day on a local database;

## v1.1.0

- monthly tracking for each category with a visual recap of daily completed tasks;

## v1.2.0

- represent non-working day (eg. saturdays and sundays) in a different color;

## v1.3.0

- represent partially completed day with different colors (eg. >25% of the expected time, >50%, >75%);
- fix a bug with data saving;
- current day in the recap should have a thicker border;

## v1.4.0

- update the montly recap as soon as a task is completed (or a percentage is reached);

## v1.5.0

- added +5'/+10'/-5'/-10' buttons to the timers;

## v2.0.0

- refactoring:

  - Trackers are now instances of the `Tracker` class, and timers are instances of the `Timer` class. This will facilitate bug solving, app maintenance and introduction of new features.
  - The `trackers` table represents all the trackers shown by the UI and the `timers` table stores the saved timer for each day and each tracker.
  - `tracker_repository` and `timer_repository` classes manage the connection to the DB and all the SQL operations to retrieve and save the data when prompted by the UI events.

- new features:
  - users can now change the month on the recap of a tracker and see the related progresses;
  - users can click on any of the squares of the recap representing a day to set the current date to that one, showing the timer saved for that day and that tracker;
  - clicking on the date label on the recap, the selected date will return to the current one;
  - only the current day timer can be modified (by starting/stoping or adding/removing minutes). The previous day timer is also editable in order to correct previous entries or allow overnight work;

## possible further features

- weekly and monthly statistics
- time spent and progress for each day (for the task) on mouse over each day of the recap canvas
- configurable trackers (with custom thresholds), the GUI should be build dynamically and all of the reference to the labels should be dynamic too;
- excel export;
