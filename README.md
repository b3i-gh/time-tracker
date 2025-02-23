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

## possible further feature

- configurable categories (with custom thresholds), the GUI should be build dynamically and all of the reference to the labels should be dynamic too;
- excel export;
