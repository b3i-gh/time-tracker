# Time Tracker

## Description

Time Tracker is a simple application to help you keep track of the time you spend on various tasks and projects;
tkinter is used for the GUI and sqlite3 for the data persistence.
You can customize the tracked tasks by modifying timer_categories and timer_thresholds (if you need to track more than 3 tasks, you should also customize the GUI).

## v1.0.0

- keeps track of 3 default categories;
- saves the timers of each day on a local database;

## v1.1.0

- monthly tracking for each category with a visual recap of daily completed tasks;

## v1.2.0

- represent non-working day (eg. saturdays and sundays) in a different color

## v1.3.0

- represent partially completed day with different colors (eg. >25% of the expected time, >50%, >75%);
- fix a bug with data saving
- current day in the recap should have a thicker border

## v1.4.0

- update the montly recap as soon as a task is completed (or a percentage is reached)


## possible further features

- configurable categories (with custom thresholds), the GUI should be build dynamically and all of the reference to the labels should be dynamic too;
- time triking over multiple days (overnight work);
- excel export;

