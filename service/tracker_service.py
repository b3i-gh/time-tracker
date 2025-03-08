from datetime import datetime, timedelta
import tkinter as tk

class Tracker_Service:
    tracker = None
    root = None
    tracker_repo = None
    timer_repo = None
    selected_date = None
    frame = None
    track_square_size = 18
    track_square_padding = 3

    def __init__(self, tracker, tracker_repo, timer_repo, root):
        self.tracker = tracker
        self.root = root
        self.tracker_repo = tracker_repo
        self.timer_repo = timer_repo
        self.selected_date = datetime.today().strftime("%Y-%m-%d").split("-")

    def draw(self):
        self.frame = tk.Frame(self.root, bd=2, relief="groove")
        self.frame.pack(padx=5, pady=5,)

        # tracker name and timer
        tk.Label(self.frame, text=(f"{self.tracker.tracker_name} ({int(self.tracker.expected_duration/60)} min)"), font=("Helvetica", 10), ).grid(row=0, column=0, pady=5,padx=5, sticky="nw", columnspan=3)
        self.tracker.timer_label = tk.Label(self.frame, text="00:00:00", font=("Arial", 30), bg="white")
        self.tracker.timer_label.grid(row=1, column=0, columnspan=3, padx=5)
        self.tracker.timer_label.bind("<Button-3>", self.show_timer_popup)
        self.update_timer()

        # start / stop buttons
        button_container = tk.Frame(self.frame)
        button_container.grid(row=2, column=0, pady=5, padx=5, sticky="ew", columnspan=3)
        self.tracker.start_button = tk.Button(button_container, text="Start", command=lambda: self.start_timer())
        button_container.grid_columnconfigure(0, weight=1)
        button_container.grid_columnconfigure(1, weight=1)
        self.tracker.start_button.grid(row=0, column=0, sticky="ew")
        self.tracker.stop_button = tk.Button(button_container, text="Stop", state="disabled", command=lambda: self.stop_timer())
        self.tracker.stop_button.grid(row=0, column=1,  sticky="ew")
        
        # montlhy recap
        self.draw_recap()

    def start_timer(self):
        if not self.tracker.timer.is_running:
            self.tracker.timer.is_running = True
            self.tracker.start_button.config(state="disabled")
            self.tracker.stop_button.config(state="normal")
            self.update_timer()

    def stop_timer(self):
        if self.tracker.timer.is_running:
            self.tracker.timer.is_running = False
            self.timer_repo.save_timer(self.tracker.timer, datetime.strptime("-".join(self.selected_date), "%Y-%m-%d"))
            self.tracker.start_button.config(state="normal")
            self.tracker.stop_button.config(state="disabled")
            self.draw_recap()

    def update_timer(self):
        if self.tracker.timer.is_running:
            self.tracker.timer.elapsed_time += 0.5
        minutes, seconds = divmod(int(self.tracker.timer.elapsed_time), 60)
        hours, minutes = divmod(minutes, 60)

        updated_timer=f"{hours:02}:{minutes:02}:{seconds:02}"
        self.tracker.timer_label.config(text=updated_timer)

        # Change style if the task is completed
        if self.tracker.timer.elapsed_time > self.tracker.expected_duration:
            self.tracker.timer_label.config(bg="green", fg="white")
        else:
            self.tracker.timer_label.config(bg="white", fg="black")

        if self.tracker.timer.is_running:
            self.root.after(500, lambda: self.update_timer())  # Update every 500ms

    def reload_timer(self):
        self.tracker.timer = self.timer_repo.get_timer_for_tracker_and_day(self.tracker.tracker_id, datetime.strptime("-".join(self.selected_date), "%Y-%m-%d"))
        self.update_timer()


    def show_timer_popup(self, event):
        if not self.tracker.timer.is_running:
            m = tk.Menu(self.root, tearoff = 0)
            m.add_command(label="+5m", command=lambda: self.add_time(5))
            m.add_command(label="+10m", command=lambda: self.add_time(10))
            m.add_separator()
            m.add_command(label="-5m", command=lambda: self.add_time(-5))
            m.add_command(label="-10m", command=lambda: self.add_time(-10))
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

    def add_time(self, minutes):
        if self.tracker.timer.elapsed_time + minutes * 60 >= 0:
            self.tracker.timer.elapsed_time += minutes * 60
            self.update_timer()
            self.timer_repo.save_timer(self.tracker.timer, datetime.strptime("-".join(self.selected_date), "%Y-%m-%d"))

    def draw_recap(self):
        selected_year = self.selected_date[0] # format: 2025
        selected_month = self.selected_date[1] # format: 03
        selected_day = self.selected_date[2] # format: 08

        month_name = datetime.strptime(selected_month, "%m").strftime("%B") # format: March
        self.tracker.recap_label = tk.Label(self.frame, text=f"{selected_day} {month_name} {selected_year}", font=("Helvetica", 8))
        self.tracker.recap_label.grid(row=3, column=1, pady=5, sticky="ew")
        self.tracker.recap_label.bind("<Button-1>", self.reset_date_to_today)
        
        self.tracker.prev_month_button = tk.Button(self.frame, text="<", command=lambda: self.change_current_month(-1))
        self.tracker.prev_month_button.grid(row=3, column=0, pady=5, padx=5, sticky="w")
       
        self.tracker.next_month_button = tk.Button(self.frame, text=">", command=lambda: self.change_current_month(1))
        self.tracker.next_month_button.grid(row=3, column=2, pady=5, padx=5, sticky="e")
       
        self.tracker.recap_canvas = tk.Canvas(self.frame)
        self.tracker.recap_canvas.update_idletasks()
        self.tracker.recap_canvas.config(width=145, height=105)

        montlhy_timers = self.timer_repo.get_monthly_timers_for_tracker(self.tracker.tracker_id, selected_month, selected_year)

        total_month_day = 31 if selected_month in ["01", "03", "05", "07", "08", "10", "12"] else 30 if selected_month in ["04", "06", "09", "11"] else 28

        for d in range(total_month_day):
            self.draw_recap_square(d, montlhy_timers, self.tracker.recap_canvas)
        
        self.tracker.recap_canvas.grid(row=4, column=0, columnspan=3)

    def draw_recap_square(self, index, daily_timers, canvas):
      
        key = str(index+1).zfill(2)
        if key in daily_timers:
            curr_timer = daily_timers[key]
            elapsed_time = curr_timer[3] 
        else:
            elapsed_time = 0
        progress = elapsed_time / self.tracker.expected_duration * 100 if elapsed_time > 0 else 0

        row, col = divmod(index, 7)
        x0, y0 = col * (self.track_square_size + self.track_square_padding) + 2, row * (self.track_square_size + self.track_square_padding) + 2
        x1, y1 = x0 + self.track_square_size, y0 + self.track_square_size

        if progress >= 100:
            color = "#1bfc02"
        elif progress > 75:
            color = "#5af948"
        elif progress > 50:
            color = "#8df981"
        elif progress > 25:
            color = "#b8f9b1"
        else:
            color = None

        outline = "black"
        ow = 1

        if self.selected_date[0] == datetime.today().strftime("%Y") and self.selected_date[1] == datetime.today().strftime("%m") and str(index+1).zfill(2) == datetime.today().strftime("%d"):
            outline = "red"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=outline, width=ow)
        
        if self.selected_date[2] == key:
            canvas.create_rectangle(x0+3, y0+3, x1-3, y1-3, fill=color, outline=outline, width=ow)
            canvas.bind("<Button-1>", self.change_current_day)

    def change_current_day(self, event):
        self.stop_timer()
        new_selected_day = str(int(event.x / (self.track_square_size + self.track_square_padding)) + 7 * int(event.y / (self.track_square_size + self.track_square_padding)) + 1).zfill(2)
        self.selected_date[2] = new_selected_day
        self.draw_recap()
        self.set_timer_status()
        self.reload_timer()

    def change_current_month(self, direction):
        self.stop_timer()
        current_year = int(self.selected_date[0])
        current_month = int(self.selected_date[1])
        
        if direction == 1:
            if current_month + direction > 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1
        else:
            if current_month + direction < 1:
                current_month = 12
                current_year -= 1
            else:
                current_month -= 1
        self.selected_date = [str(current_year), str(current_month).zfill(2), "01"]
        self.draw_recap()
        self.set_timer_status()
        self.reload_timer()

    def reset_date_to_today(self, _):
        self.stop_timer()
        self.selected_date = datetime.today().strftime("%Y-%m-%d").split("-")
        self.draw_recap()
        self.set_timer_status()
        self.reload_timer()

    def set_timer_status(self):
        today = datetime.today()
        selected_date = datetime.strptime("-".join(self.selected_date), "%Y-%m-%d")
        yesterday = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        if selected_date.date() in [today.date(), yesterday.date()]:
            self.tracker.start_button.config(state="normal")
            self.tracker.stop_button.config(state="normal" if self.tracker.timer.is_running else "disabled")
            self.tracker.timer_label.bind("<Button-3>", self.show_timer_popup)
        else:
            self.tracker.start_button.config(state="disabled")
            self.tracker.stop_button.config(state="disabled")
            self.tracker.timer_label.unbind("<Button-3>")
