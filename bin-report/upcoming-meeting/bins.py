import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime, timedelta
import pandas as pd
import os
from tkcalendar import Calendar
from sqlalchemy import create_engine
from contextlib import contextmanager

prefix_list = [
    "CC6.Bin_BRight",
    "CC7.Bin_BRight",
    "CC8.Bin_BLeft",
    "CC8.Bin_BRight",
    "CC9.Bin_BRight",
    "CC10.Bin_BLeft",
    "CC10.Bin_BRight",
    "CC11.Bin_BRight",
    "CC12.Bin_BLeft",
    "CC12.Bin_BRight",
    "CC13.Bin_BRight",
    "CC14.Bin_BLeft",
    "CC14.Bin_BRight",
    "CC15.Bin_BRight",
    "CC16.Bin_BLeft",
    "CC16.Bin_BRight",
    "CC17.Bin_BRight",
    "CC18.Bin_BLeft",
    "CC18.Bin_BRight",
    "CC19.Bin_BRight",
    "CC20.Bin_BLeft",
    "CC20.Bin_BRight",
    "CC21.Bin_BRight",
    "CC22.Bin_BLeft",
    "CC22.Bin_BRight",
    "CC23.Bin_BRight",
    "CC24.Bin_BLeft",
    "CC24.Bin_BRight",
    "CC25.Bin_BRight",
    "CC26.Bin_BLeft",
    "CC26.Bin_BRight",
    "CC27.Bin_BRight",
    "CC28.Bin_BLeft",
    "CC28.Bin_BRight",
    "CC29.Bin_BRight",
    "CC30.Bin_BLeft",
    "CC30.Bin_BRight",
    "CC31.Bin_BRight",
    "CC32.Bin_BLeft",
    "CC32.Bin_BRight",
    "CC36.Bin_BLeft",
    "CC36.Bin_BRight",
    "CC37.Bin_BRight",
    "CC38.Bin_BLeft",
    "CC38.Bin_BRight",
    "CC39.Bin_BRight",
    "CC40.Bin_BLeft",
    "CC40.Bin_BRight",
    "CC41.Bin_BRight",
    "CC42.Bin_BLeft",
    "CC42.Bin_BRight",
    "CC43.Bin_BRight",
    "CC44.Bin_BLeft",
    "CC44.Bin_BRight",
    "CC45.Bin_BRight",
    "CC46.Bin_BLeft",
    "CC46.Bin_BRight",
    "CC47.Bin_BRight",
    "CC48.Bin_BLeft",
    "CC48.Bin_BRight",
    "CC49.Bin_BRight",
    "CC50.Bin_BLeft",
    "CC50.Bin_BRight",
    "CC51.Bin_BRight",
    "CC52.Bin_BLeft",
    "CC52.Bin_BRight",
    "CC53.Bin_BRight",
    "CC54.Bin_BLeft",
    "CC54.Bin_BRight",
    "CC55.Bin_BRight",
    "CC56.Bin_BLeft",
    "CC56.Bin_BRight",
    "CC57.Bin_BRight",
    "CC58.Bin_BLeft",
    "CC58.Bin_BRight",
    "CC59.Bin_BRight",
    "CC60.Bin_BLeft",
    "CC60.Bin_BRight",
    "CC61.Bin_BRight",
    "CC62.Bin_BLeft",
    "CC62.Bin_BRight",
    "CC63.Bin_BRight",
    "CC64.Bin_BLeft",
    "CC64.Bin_BRight",
    "CC65.Bin_BRight",
    "CC66.Bin_BLeft",
    "CC66.Bin_BRight",
    "CC67.Bin_BRight",
    "CC68.Bin_BLeft",
    "CC68.Bin_BRight",
    "CC69.Bin_BRight",
    "CC70.Bin_BLeft",
    "CC70.Bin_BRight",
    "CC71.Bin_BRight",
    "CC72.Bin_BLeft",
    "CC72.Bin_BRight",
    "CC73.Bin_BRight",
    "CC74.Bin_BLeft",
    "CC74.Bin_BRight",
    "CC75.Bin_BRight",
    "CC76.Bin_BLeft",
    "CC76.Bin_BRight",
    "CC77.Bin_BRight"
]

suffixes = ["_Full", "_NotPresent", "_PresentNotResumed"]

NUM_HOURS = 24

def build_intervals_per_alarm(df_alarm):
    """
    Given a DataFrame of rows for ONE point_id, each row has:
       - 'timestamp': the time
       - '_VAL': 0 or 1
    Build intervals where alarm is active from (_VAL=1) to (_VAL=0).
    Returns a list of (start_ts, end_ts) tuples.
    """
    intervals = []
    active_start = None
    for _, row in df_alarm.iterrows():
        val = row['_VAL']
        ts = row['timestamp']
        if val == 1:
            # alarm ON
            active_start = ts
        else:
            # alarm OFF
            if active_start is not None:
                intervals.append((active_start, ts))
                active_start = None
    return intervals

def split_into_hourly_buckets(start_time, end_time, hourly_intervals):
    """
    Split a given (start_time, end_time) interval into the provided
    hourly_intervals = [(hour0_start, hour0_end), (hour1_start, hour1_end), ...].
    Return a dict {i: [downtime_seconds, trigger_count]} for each hour index i.
    
    'trigger_count' is incremented if the interval STARTS in that hour.
    """
    bucket_data = {i: [0.0, 0] for i in range(len(hourly_intervals))}
    
    for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
        overlap_start = max(start_time, bucket_start)
        overlap_end   = min(end_time, bucket_end)
        
        if overlap_end > overlap_start:
            overlap_seconds = (overlap_end - overlap_start).total_seconds()
            bucket_data[i][0] += overlap_seconds  # downtime
            
            # If the interval STARTS in this bucket, increment the "trigger" count
            if bucket_start <= start_time < bucket_end:
                bucket_data[i][1] += 1
    return bucket_data

class DatabaseQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CIMPLICITY Database Query")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Adjust your connection string as needed
        self.conn_str = (
            "mssql+pyodbc://sa:Retiina1B@192.168.165.10\\SQLEXPRESS/"
            "CIMPLICITY?driver=ODBC+Driver+17+for+SQL+Server"
        )
        self.engine = None
        
        self.connect_db()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    @contextmanager
    def get_connection(self):
        """Use a context manager for DB connections."""
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        finally:
            if connection:
                connection.close()

    def connect_db(self):
        """Test the DB connection once at startup."""
        from sqlalchemy import create_engine
        try:
            self.engine = create_engine(self.conn_str)
            with self.engine.connect() as conn:
                pass
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.root.quit()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        date_frame = ttk.LabelFrame(main_frame, text="Date & Time Range", padding=10)
        date_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        start_frame = ttk.Frame(date_frame)
        start_frame.grid(row=0, column=0, padx=5)
        ttk.Label(start_frame, text="Start Date:").grid(row=0, column=0, pady=5)

        # default to yesterday
        today = datetime.now()
        yesterday = today - timedelta(days=1)

        self.start_date = Calendar(
            start_frame, 
            selectmode='day', 
            date_pattern='y-mm-dd',
            year=yesterday.year,
            month=yesterday.month,
            day=yesterday.day
        )
        self.start_date.grid(row=1, column=0)

        ttk.Label(start_frame, text="Start Time (HH:MM:SS):").grid(row=2, column=0, pady=(10, 0))
        time_spinbox_frame = ttk.Frame(start_frame)
        time_spinbox_frame.grid(row=3, column=0, pady=5)

        self.start_hour   = tk.StringVar(value="07")
        self.start_minute = tk.StringVar(value="00")
        self.start_second = tk.StringVar(value="00")

        self.start_hour_sb = ttk.Spinbox(
            time_spinbox_frame, from_=0, to=23, wrap=True, 
            textvariable=self.start_hour, width=3, format="%02.0f"
        )
        self.start_hour_sb.pack(side=tk.LEFT)
        ttk.Label(time_spinbox_frame, text=":").pack(side=tk.LEFT)

        self.start_minute_sb = ttk.Spinbox(
            time_spinbox_frame, from_=0, to=59, wrap=True, 
            textvariable=self.start_minute, width=3, format="%02.0f"
        )
        self.start_minute_sb.pack(side=tk.LEFT)
        ttk.Label(time_spinbox_frame, text=":").pack(side=tk.LEFT)

        self.start_second_sb = ttk.Spinbox(
            time_spinbox_frame, from_=0, to=59, wrap=True, 
            textvariable=self.start_second, width=3, format="%02.0f"
        )
        self.start_second_sb.pack(side=tk.LEFT)

        end_frame = ttk.Frame(date_frame)
        end_frame.grid(row=0, column=1, padx=5)
        ttk.Label(end_frame, text="End Date:").grid(row=0, column=0, pady=5)

        self.end_date = Calendar(
            end_frame, 
            selectmode='day', 
            date_pattern='y-mm-dd',
            year=today.year,
            month=today.month,
            day=today.day
        )
        self.end_date.grid(row=1, column=0)

        ttk.Label(end_frame, text="End Time (HH:MM:SS):").grid(row=2, column=0, pady=(10, 0))
        time_spinbox_frame2 = ttk.Frame(end_frame)
        time_spinbox_frame2.grid(row=3, column=0, pady=5)

        self.end_hour   = tk.StringVar(value="06")
        self.end_minute = tk.StringVar(value="59")
        self.end_second = tk.StringVar(value="59")

        self.end_hour_sb = ttk.Spinbox(
            time_spinbox_frame2, from_=0, to=23, wrap=True, 
            textvariable=self.end_hour, width=3, format="%02.0f"
        )
        self.end_hour_sb.pack(side=tk.LEFT)
        ttk.Label(time_spinbox_frame2, text=":").pack(side=tk.LEFT)

        self.end_minute_sb = ttk.Spinbox(
            time_spinbox_frame2, from_=0, to=59, wrap=True, 
            textvariable=self.end_minute, width=3, format="%02.0f"
        )
        self.end_minute_sb.pack(side=tk.LEFT)
        ttk.Label(time_spinbox_frame2, text=":").pack(side=tk.LEFT)

        self.end_second_sb = ttk.Spinbox(
            time_spinbox_frame2, from_=0, to=59, wrap=True, 
            textvariable=self.end_second, width=3, format="%02.0f"
        )
        self.end_second_sb.pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        self.query_button = ttk.Button(button_frame, text="Run Query & Process", command=self.query_and_process)
        self.query_button.pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=2, column=0, pady=5)

    def validate_dates(self):
        """Ensure start_date <= end_date and that they're valid."""
        try:
            start_dt_str = f"{self.start_date.selection_get().strftime('%Y-%m-%d')} {self.start_hour.get()}:{self.start_minute.get()}:{self.start_second.get()}"
            end_dt_str   = f"{self.end_date.selection_get().strftime('%Y-%m-%d')} {self.end_hour.get()}:{self.end_minute.get()}:{self.end_second.get()}"
            
            start_date = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M:%S")
            end_date   = datetime.strptime(end_dt_str, "%Y-%m-%d %H:%M:%S")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return None, None, False
        
        if start_date > end_date:
            messagebox.showerror("Error", "Start date/time must be before end date/time")
            return None, None, False
        
        return start_date, end_date, True

    def query_and_process(self):
        """Main entry point after user clicks 'Run Query & Process'."""

        start_date, end_date, is_valid = self.validate_dates()
        if not is_valid:
            return
        
        self.query_button.state(['disabled'])
        self.progress_var.set("Querying database...")
        self.root.update_idletasks()
        
        try:
            query = """
                SELECT 
                    [timestamp], 
                    [point_id],
                    [_VAL]
                FROM [CIMPLICITY].[dbo].[DATA_LOG]
                WHERE point_id LIKE 'CC%'
                  AND [timestamp] BETWEEN ? AND ?
                ORDER BY [timestamp] ASC
            """
            
            with self.get_connection() as conn:
                df = pd.read_sql(query, conn, params=(start_date, end_date))
            
            if df.empty:
                messagebox.showinfo("Info", "No data found for the selected date/time range.")
                return

            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['_VAL'] = df['_VAL'].fillna(0).astype(int)

            self.progress_var.set("Processing bin-full logic...")
            self.root.update_idletasks()
            self.run_bin_full_logic(df)

            # Done
            self.progress_var.set("Done! Created hourly-trigger.csv and hourly-downtime.csv")
            messagebox.showinfo("Success", "Processing complete. CSV files saved.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.query_button.state(['!disabled'])

    def run_bin_full_logic(self, df):
        """
        This replaces the second script’s main() function. 
        It filters df to the needed point_ids, builds intervals, 
        and outputs hourly-trigger.csv and hourly-downtime.csv.
        """

        all_alarms = []
        prefix_to_sub_alarms = {}
        for prefix in prefix_list:
            sub_alarms = [prefix + sfx for sfx in suffixes]
            prefix_to_sub_alarms[prefix] = sub_alarms
            all_alarms.extend(sub_alarms)
        
        df = df[df['point_id'].isin(all_alarms)]
        if df.empty:
            return

        df = df.sort_values(by='timestamp')

        min_date = df['timestamp'].min().floor('D')
        start_of_day = min_date.replace(hour=7, minute=0, second=0, microsecond=0)
        
        hourly_intervals = []
        current = start_of_day
        for i in range(NUM_HOURS):
            next_hour = current + pd.Timedelta(hours=1)
            hourly_intervals.append((current, next_hour))
            current = next_hour
        
        def format_hour_label(ts):
            return ts.strftime('%H:%M')
        
        interval_labels = [format_hour_label(s) for (s, e) in hourly_intervals]
        count_cols = [lbl + "_count" for lbl in interval_labels]
        downtime_cols = [lbl + "_downtime" for lbl in interval_labels]

        alarm_hour_data = {
            prefix: {i: [0.0, 0] for i in range(NUM_HOURS)}
            for prefix in prefix_list
        }

        def accumulate_intervals(prefix, intervals, add_triggers=False):
            """
            prefix: e.g. 'CC6.Bin_BRight'
            intervals: list of (start_ts, end_ts)
            add_triggers: if True, we count triggers
            """
            day_start = hourly_intervals[0][0]
            day_end   = hourly_intervals[-1][1]  # up to 7:00 next day

            for (start_ts, end_ts) in intervals:
                if end_ts <= day_start or start_ts >= day_end:
                    continue

                st = max(start_ts, day_start)
                en = min(end_ts, day_end)
                
                bucket_dict = split_into_hourly_buckets(st, en, hourly_intervals)
                for i in range(NUM_HOURS):
                    # downtime
                    alarm_hour_data[prefix][i][0] += bucket_dict[i][0]
                    # triggers
                    if add_triggers:
                        alarm_hour_data[prefix][i][1] += bucket_dict[i][1]

        for prefix in prefix_list:
            sub_alarms = prefix_to_sub_alarms[prefix]
            # e.g. [prefix+'_Full', prefix+'_NotPresent', prefix+'_PresentNotResumed']

            intervals_map = {}
            for point_id in sub_alarms:
                df_sub = df[df['point_id'] == point_id]
                if df_sub.empty:
                    intervals_map[point_id] = []
                    continue
                intervals_map[point_id] = build_intervals_per_alarm(df_sub)

            # accumulate intervals
            for point_id in sub_alarms:
                add_trigs = (point_id.endswith("_Full"))
                intervals = intervals_map[point_id]
                accumulate_intervals(prefix, intervals, add_triggers=add_trigs)

        rows = []
        for prefix in prefix_list:
            row_dict = {"point_id": prefix}
            for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
                sec  = alarm_hour_data[prefix][i][0]  # downtime seconds
                trig = alarm_hour_data[prefix][i][1]  # trigger count
                row_dict[count_cols[i]] = trig
                row_dict[downtime_cols[i]] = sec
            rows.append(row_dict)

        results = pd.DataFrame(rows)
        results['sort_order'] = results['point_id'].apply(lambda x: prefix_list.index(x))
        results = results.sort_values('sort_order').drop(columns=['sort_order'])

        # 1) trigger counts
        results_counts = results[['point_id'] + count_cols].copy()
        rename_map_counts = {c: c.replace("_count", "") for c in count_cols}
        results_counts = results_counts.rename(columns=rename_map_counts)
        counts_csv = os.path.join(self.current_dir, "hourly-trigger.csv")
        results_counts.to_csv(counts_csv, index=False)

        # 2) downtime
        results_downtime = results[['point_id'] + downtime_cols].copy()
        rename_map_downtime = {c: c.replace("_downtime", "") for c in downtime_cols}
        results_downtime = results_downtime.rename(columns=rename_map_downtime)
        downtime_csv = os.path.join(self.current_dir, "hourly-downtime.csv")
        results_downtime.to_csv(downtime_csv, index=False)
        
        print("Created:", counts_csv)
        print("Created:", downtime_csv)

    def on_closing(self):
        if self.engine:
            self.engine.dispose()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseQueryApp(root)
    root.mainloop()
