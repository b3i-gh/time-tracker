import tkinter as tk
import time
import sqlite3

class TimeTrackerApp:
    timer_categories = ["Coding", "Study", "Personal"]
    timer_thresholds = [180, 120, 60]

    def load_initial_timers(self):
        connection = sqlite3.connect('time-tracker.db')
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

    def save_timer(self, i):
        task = self.timer_categories[i]
        expected_duration = self.timer_thresholds[i]
        date = time.strftime("%Y-%m-%d")
        time_spent = self.elapsed_time[i]
        completed = 1 if self.elapsed_time[i] >= expected_duration else 0
        
        # check if there is an existing timer for today for this category
        connection = sqlite3.connect('time-tracker.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM timers WHERE task = ? AND date = ?", (task, date))
        timer_id = cursor.fetchone()
        connection.close()

        if timer_id:
            try:
                connection = sqlite3.connect('time-tracker.db')
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
                connection = sqlite3.connect('time-tracker.db')
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

    def update_timer(self, i):
        self.elapsed_time[i] = time.time() - self.start_time[i]
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
        if self.elapsed_time[i] > self.timer_thresholds[i]:
            label.config(bg="green", fg="white")
        else:
            label.config(bg="white", fg="black")

        if self.running[i]:
            self.root.after(1000, lambda: self.update_timer(i))  # Update every 1000ms

    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        root.title("Time Tracker")
        self.running = [False, False, False]
        self.elapsed_time = [0, 0, 0]
        self.start_time = [None, None, None]

        self.frame_coding = tk.Frame(bd=2, relief="groove")
        self.frame_coding.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, )
        tk.Label(self.frame_coding, text="Coding (180m)", font=("Helvetica", 10), ).grid(row=0, column=0, pady=5, sticky="nw", columnspan=2)
        self.label_coding_timer = tk.Label(self.frame_coding, text="00:00:00", font=("Arial", 30), bg="white")
        self.label_coding_timer.grid(row=1, column=0, columnspan=2)
        tk.Button(self.frame_coding, text="Start", command=lambda: self.start_timer(0)).grid(row=2, column=0, sticky="nsew")
        tk.Button(self.frame_coding, text="Stop", command=lambda: self.stop_timer(0)).grid(row=2, column=1,  sticky="nsew")

        self.frame_study = tk.Frame(bd=2, relief="groove")
        self.frame_study.grid(row=1, column=0, sticky="nsew", padx=5, pady=5,)
        tk.Label(self.frame_study, text="Study (120m)", font=("Helvetica", 10), ).grid(row=0, column=0, pady=5, sticky="nw", columnspan=2)
        self.label_study_timer = tk.Label(self.frame_study, text="00:00:00", font=("Arial", 30), bg="white")
        self.label_study_timer.grid(row=1, column=0, columnspan=2)
        tk.Button(self.frame_study, text="Start", command=lambda: self.start_timer(1)).grid(row=2, column=0, sticky="nsew")
        tk.Button(self.frame_study, text="Stop", command=lambda: self.stop_timer(1)).grid(row=2, column=1,  sticky="nsew")

        self.frame_personal = tk.Frame(bd=2, relief="groove")
        self.frame_personal.grid(row=2, column=0, sticky="nsew", padx=5, pady=5,)
        tk.Label(self.frame_personal, text="Personal (60m)", font=("Helvetica", 10), ).grid(row=0, column=0, pady=5, sticky="nw", columnspan=2)
        self.label_personal_timer = tk.Label(self.frame_personal, text="00:00:00", font=("Arial", 30), bg="white")
        self.label_personal_timer.grid(row=1, column=0, columnspan=2)
        tk.Button(self.frame_personal, text="Start", command=lambda: self.start_timer(2)).grid(row=2, column=0, sticky="nsew")
        tk.Button(self.frame_personal, text="Stop", command=lambda: self.stop_timer(2)).grid(row=2, column=1,  sticky="nsew")

        self.create_test_tables()
        self.load_initial_timers()

    def create_test_tables(self):
        connection = sqlite3.connect('time-tracker.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS timers (
                            id INTEGER PRIMARY KEY,
                            task TEXT NOT NULL,
                            expected_duration INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            time_spent INTEGER NOT NULL,
                            completed INTEGER NOT NULL
                        )''')
        connection.commit()
        connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
