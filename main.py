import tkinter as tk
import time
import sqlite3
from datetime import datetime, timedelta

class TimeTrackerApp:
    timer_thresholds = [10800, 7200, 3600]
    # current_db = 'time-tracker.db'
    current_db = 'time-tracker-dev.db'

    track_cols = 7 
    track_square_size = 18
    track_square_padding = 3


    def load_initial_timers(self):
        connection = sqlite3.connect(self.current_db)
        cursor = connection.cursor()
        cursor.execute("SELECT task, time_spent FROM timers WHERE date = ?", (time.strftime("%Y-%m-%d"),))
        timers = cursor.fetchall()
        connection.close()

        for task, time_spent in timers:
            if task == "Coding":
                i = 0
            elif task == "Study":
                i = 1
            elif task == "Personal":
                i = 2

            self.running[i] = False
            self.start_time[i] = time.time() - time_spent
            self.elapsed_time[i] = time_spent
            self.update_timer(i)

    def load_monthly_tasks(self, task_name):
        connection = sqlite3.connect(self.current_db)
        cursor = connection.cursor()
        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute("SELECT date, expected_duration, time_spent FROM timers WHERE task = ? AND date LIKE ?", (task_name, f"{current_month}-%"))
        data = cursor.fetchall()
        data = {int(row[0].split("-")[2]): row for row in data}
        connection.close()
        return data

    # Draw a square in the track
    def draw_track_square(self, i, progress, canvas):
        row, col = divmod(i, self.track_cols)
        x0, y0 = col * (self.track_square_size + self.track_square_padding) + 2, row * (self.track_square_size + self.track_square_padding) + 2
        x1, y1 = x0 + self.track_square_size, y0 + self.track_square_size
        
        day_of_week = (datetime.today().replace(day=1) + timedelta(days=i)).weekday()
        
        if progress >= 100:
            color = "#1bfc02"
        elif progress > 75:
            color = "#5af948"
        elif progress > 50:
            color = "#8df981"
        elif progress > 25:
            color = "#b8f9b1"
        elif day_of_week == 5 or day_of_week == 6:
            color = "grey"
        else:
            color = None

        outline = "black"
        ow = 1
        if i+1 == datetime.now().day:
            outline = "red"
            ow = 2
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=outline, width=ow) 

    # Draw the recap track 
    def draw_recap(self, task_name, canvas):
        data = self.load_monthly_tasks(task_name)

        current_month = datetime.now().month
        total_month_day = 31 if current_month in [1, 3, 5, 7, 8, 10, 12] else 30 if current_month in [4, 6, 9, 11] else 28

        for i in range(total_month_day):
            curr_day_data = data[i+1] if i+1 in data else None
            expected_duration = curr_day_data[1] if curr_day_data else 0
            time_spent = curr_day_data[2] if curr_day_data else 0
            progress = time_spent / expected_duration * 100 if time_spent > 0 else 0
            self.draw_track_square(i, progress, canvas)
            

    def save_timer(self, i):
        task = self.timer_categories[i]
        expected_duration = self.timer_thresholds[i]
        date = time.strftime("%Y-%m-%d")
        time_spent = self.elapsed_time[i]
        completed = 1 if self.elapsed_time[i] >= expected_duration else 0
        
        # check if there is an existing timer for today for this category
        connection = sqlite3.connect(self.current_db)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM timers WHERE task = ? AND date = ?", (task, date))
        timer_id = cursor.fetchone()
        connection.close()

        if timer_id:
            try:
                connection = sqlite3.connect(self.current_db)
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE timers
                    SET time_spent = ?, completed = ?
                    WHERE id = ?
                """, (time_spent, completed, timer_id[0]))
                connection.commit()
                connection.close()
            except sqlite3.Error as e:
                raise Exception(f"Errore durante il salvataggio del timer")
        else:
            try:
                connection = sqlite3.connect(self.current_db)
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO timers (task, expected_duration, date, time_spent, completed)
                    VALUES (?, ?, ?, ?, ?)
                """, (task, expected_duration, date, time_spent, completed))

                connection.commit()
                connection.close()
            except sqlite3.Error as e:
                raise Exception(f"Errore durante il salvataggio del timer")

    def start_timer(self, i):
        if not self.running[i]:
            self.running[i] = True
            self.start_time[i] = time.time() - self.elapsed_time[i]
            self.update_timer(i)

    def stop_timer(self, i):
        if self.running[i]:
            self.running[i] = False
            self.elapsed_time[i] = time.time() - self.start_time[i]
            self.save_timer(i)

    def update_timer(self, i, elapsed_time=None):
        starting_time = self.start_time[i] if self.start_time[i] else 0
        if elapsed_time != None:
            self.elapsed_time[i] = elapsed_time
        else:
            self.elapsed_time[i] = time.time() - starting_time
        minutes, seconds = divmod(int(self.elapsed_time[i]), 60)
        hours, minutes = divmod(minutes, 60)
        updated_timer=f"{hours:02}:{minutes:02}:{seconds:02}"

        if i == 0:
            label = self.label_coding_timer
        elif i == 1:
            label = self.label_study_timer
        elif i == 2:
            label = self.label_personal_timer

        label.config(text=updated_timer)

        # Change style if the task is completed
        expected_duration = self.timer_thresholds[i]
        time_spent = self.elapsed_time[i]
        if time_spent > expected_duration:
            label.config(bg="green", fg="white")
        else:
            label.config(bg="white", fg="black")

        progress = time_spent / expected_duration * 100 if time_spent > 0 else 0
        canvas = None
        if i == 0:
            canvas = self.frame_coding.winfo_children()[4]
        elif i == 1:
            canvas = self.frame_study.winfo_children()[4]
        elif i == 2:
            canvas = self.frame_personal.winfo_children()[4]
        self.draw_track_square(datetime.now().day-1, progress, canvas)

        if self.running[i]:
            self.root.after(1000, lambda: self.update_timer(i))  # Update every 1000ms

    def add_time(self, minutes, i):
        if self.elapsed_time[i] + minutes * 60 >= 0:
            self.elapsed_time[i] += minutes * 60
            self.update_timer(i, self.elapsed_time[i])
            self.save_timer(i)
    
    def do_popup(self, event):
        widget = event.widget
        if widget == self.label_coding_timer:
            i = 0
        elif widget == self.label_study_timer:
            i = 1
        elif widget == self.label_personal_timer:
            i = 2

        if not self.running[i]:
            m = tk.Menu(self.root, tearoff = 0)
            m.add_command(label="+5m", command=lambda: self.add_time(5, i))
            m.add_command(label="+10m", command=lambda: self.add_time(10, i))
            m.add_separator()
            m.add_command(label="-5m", command=lambda: self.add_time(-5, i))
            m.add_command(label="-10m", command=lambda: self.add_time(-10, i))
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

    def __init__(self, root):
        self.create_test_tables()
        self.root = root
        self.root.title("Time Tracker")
        root.title("Time Tracker")
        self.running = [False, False, False]
        self.timer_categories = ["Coding", "Study", "Personal"]
        self.elapsed_time = [0, 0, 0]
        self.start_time = [None, None, None]

        self.frame_coding = tk.Frame(bd=2, relief="groove")
        self.frame_coding.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, )
        tk.Label(self.frame_coding, text="Coding (180m)", font=("Helvetica", 10), ).grid(row=0, column=0, pady=5, sticky="nw", columnspan=2)
        self.label_coding_timer = tk.Label(self.frame_coding, text="00:00:00", font=("Arial", 30), bg="white")
        self.label_coding_timer.grid(row=1, column=0, columnspan=2)
        self.label_coding_timer.bind("<Button-3>", self.do_popup)
        tk.Button(self.frame_coding, text="Start", command=lambda: self.start_timer(0)).grid(row=2, column=0, sticky="nsew")
        tk.Button(self.frame_coding, text="Stop", command=lambda: self.stop_timer(0)).grid(row=2, column=1,  sticky="nsew")
        canvas_coding = tk.Canvas(self.frame_coding)
        canvas_coding.update_idletasks()
        canvas_coding.config(width=160, height=98)
        canvas_coding.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        self.draw_recap("Coding", canvas_coding)

        self.frame_study = tk.Frame(bd=2, relief="groove")
        self.frame_study.grid(row=1, column=0, sticky="nsew", padx=5, pady=5,)
        tk.Label(self.frame_study, text="Study (120m)", font=("Helvetica", 10), ).grid(row=0, column=0, pady=5, sticky="nw", columnspan=2)
        self.label_study_timer = tk.Label(self.frame_study, text="00:00:00", font=("Arial", 30), bg="white")
        self.label_study_timer.grid(row=1, column=0, columnspan=2)
        self.label_study_timer.bind("<Button-3>", self.do_popup)
        tk.Button(self.frame_study, text="Start", command=lambda: self.start_timer(1)).grid(row=2, column=0, sticky="nsew")
        tk.Button(self.frame_study, text="Stop", command=lambda: self.stop_timer(1)).grid(row=2, column=1,  sticky="nsew")
        canvas_study = tk.Canvas(self.frame_study)
        canvas_study.update_idletasks()
        canvas_study.config(width=160, height=98)
        canvas_study.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        self.draw_recap("Study", canvas_study)

        self.frame_personal = tk.Frame(bd=2, relief="groove")
        self.frame_personal.grid(row=2, column=0, sticky="nsew", padx=5, pady=5,)
        tk.Label(self.frame_personal, text="Personal (60m)", font=("Helvetica", 10), ).grid(row=0, column=0, pady=5, sticky="nw", columnspan=2)
        self.label_personal_timer = tk.Label(self.frame_personal, text="00:00:00", font=("Arial", 30), bg="white")
        self.label_personal_timer.grid(row=1, column=0, columnspan=2)
        self.label_personal_timer.bind("<Button-3>", self.do_popup)
        tk.Button(self.frame_personal, text="Start", command=lambda: self.start_timer(2)).grid(row=2, column=0, sticky="nsew")
        tk.Button(self.frame_personal, text="Stop", command=lambda: self.stop_timer(2)).grid(row=2, column=1,  sticky="nsew")
        canvas_personal = tk.Canvas(self.frame_personal)
        canvas_personal.update_idletasks()
        canvas_personal.config(width=160, height=98)
        canvas_personal.grid(row=3, column=0, columnspan=2, pady=5, sticky="nsew")
        self.draw_recap("Personal", canvas_personal)

        self.load_initial_timers()

    def create_test_tables(self):
        connection = sqlite3.connect(self.current_db)
        cursor = connection.cursor()

        if self.current_db == 'time-tracker-dev.db':
            cursor.execute('''DROP TABLE timers''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS timers (
                            id INTEGER PRIMARY KEY,
                            task TEXT NOT NULL,
                            expected_duration INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            time_spent INTEGER NOT NULL,
                            completed INTEGER NOT NULL
                        )''')
            cursor.execute('''INSERT OR IGNORE INTO timers (task, expected_duration, date, time_spent, completed)
                          VALUES ("Coding", 10800, "2025-02-01", 5213, 0)''')
            cursor.execute('''INSERT OR IGNORE INTO timers (task, expected_duration, date, time_spent, completed)
                          VALUES ("Coding", 10800, "2025-02-03", 8213, 0)''')
            cursor.execute('''INSERT OR IGNORE INTO timers (task, expected_duration, date, time_spent, completed)
                          VALUES ("Study", 7200, "2025-02-02", 4500, 0)''')   
            cursor.execute('''INSERT OR IGNORE INTO timers (task, expected_duration, date, time_spent, completed)
                          VALUES ("Personal", 3600, "2025-02-03", 3600, 1)''') 
            cursor.execute('''INSERT OR IGNORE INTO timers (task, expected_duration, date, time_spent, completed)
                          VALUES ("Personal", 3600, "2025-02-04", 3500, 0)''') 
            cursor.execute('''INSERT OR IGNORE INTO timers (task, expected_duration, date, time_spent, completed)
                          VALUES ("Personal", 3600, "2025-02-05", 1900, 0)''') 
            cursor.execute('''INSERT OR IGNORE INTO timers (task, expected_duration, date, time_spent, completed)
                          VALUES ("Personal", 3600, "2025-02-06", 1000, 0)''') 
        
        connection.commit()
        connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
