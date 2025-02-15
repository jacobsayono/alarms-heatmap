import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime, timedelta
import pandas as pd
import os
from tkcalendar import Calendar
from sqlalchemy import create_engine
from contextlib import contextmanager
import openpyxl

class DatabaseQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CIMPLICITY Database Query")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.conn_str = 'mssql+pyodbc://sa:Retiina1B@192.168.165.10\\SQLEXPRESS/CIMPLICITY?driver=ODBC+Driver+17+for+SQL+Server'
        self.engine = None
        self.connect_db()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect_db(self):
        try:
            self.engine = create_engine(self.conn_str)
            with self.engine.connect() as conn:
                pass
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {str(e)}")
            self.root.quit()
            
    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        finally:
            if connection:
                connection.close()

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        date_frame = ttk.LabelFrame(main_frame, text="Date & Time Range", padding=10)
        date_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        start_frame = ttk.Frame(date_frame)
        start_frame.grid(row=0, column=0, padx=5)
        ttk.Label(start_frame, text="Start Date:").grid(row=0, column=0, pady=5)

        self.start_date = Calendar(
            start_frame, 
            selectmode='day', 
            date_pattern='y-mm-dd'

            year=yesterday.year,
            month=yesterday.month,
            day=yesterday.day
        )
        self.start_date.grid(row=1, column=0)

        time_label = ttk.Label(start_frame, text="Start Time (HH:MM:SS):")
        time_label.grid(row=2, column=0, pady=(10, 0))

        time_spinbox_frame = ttk.Frame(start_frame)
        time_spinbox_frame.grid(row=3, column=0, pady=5)

        self.start_hour = tk.StringVar(value="07")
        self.start_hour_sb = ttk.Spinbox(
            time_spinbox_frame, 
            from_=0, to=23, 
            wrap=True, 
            textvariable=self.start_hour,
            width=3,
            format="%02.0f"
        )
        self.start_hour_sb.pack(side=tk.LEFT)

        ttk.Label(time_spinbox_frame, text=":").pack(side=tk.LEFT)

        self.start_minute = tk.StringVar(value="00")
        self.start_minute_sb = ttk.Spinbox(
            time_spinbox_frame, 
            from_=0, to=59, 
            wrap=True, 
            textvariable=self.start_minute,
            width=3,
            format="%02.0f"
        )
        self.start_minute_sb.pack(side=tk.LEFT)

        ttk.Label(time_spinbox_frame, text=":").pack(side=tk.LEFT)

        self.start_second = tk.StringVar(value="00")
        self.start_second_sb = ttk.Spinbox(
            time_spinbox_frame, 
            from_=0, to=59, 
            wrap=True, 
            textvariable=self.start_second,
            width=3,
            format="%02.0f"
        )
        self.start_second_sb.pack(side=tk.LEFT)

        end_frame = ttk.Frame(date_frame)
        end_frame.grid(row=0, column=1, padx=5)
        ttk.Label(end_frame, text="End Date:").grid(row=0, column=0, pady=5)

        self.end_date = Calendar(
            end_frame, 
            selectmode='day', 
            date_pattern='y-mm-dd'
        )
        self.end_date.grid(row=1, column=0)

        time_label = ttk.Label(end_frame, text="End Time (HH:MM:SS):")
        time_label.grid(row=2, column=0, pady=(10, 0))

        time_spinbox_frame = ttk.Frame(end_frame)
        time_spinbox_frame.grid(row=3, column=0, pady=5)

        self.end_hour = tk.StringVar(value="06")
        self.end_hour_sb = ttk.Spinbox(
            time_spinbox_frame, 
            from_=0, to=23, 
            wrap=True, 
            textvariable=self.end_hour,
            width=3,
            format="%02.0f"
        )
        self.end_hour_sb.pack(side=tk.LEFT)

        ttk.Label(time_spinbox_frame, text=":").pack(side=tk.LEFT)

        self.end_minute = tk.StringVar(value="59")
        self.end_minute_sb = ttk.Spinbox(
            time_spinbox_frame, 
            from_=0, to=59, 
            wrap=True, 
            textvariable=self.end_minute,
            width=3,
            format="%02.0f"
        )
        self.end_minute_sb.pack(side=tk.LEFT)

        ttk.Label(time_spinbox_frame, text=":").pack(side=tk.LEFT)

        self.end_second = tk.StringVar(value="59")
        self.end_second_sb = ttk.Spinbox(
            time_spinbox_frame, 
            from_=0, to=59, 
            wrap=True, 
            textvariable=self.end_second,
            width=3,
            format="%02.0f"
        )
        self.end_second_sb.pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        self.query_button = ttk.Button(button_frame, text="Run Query & Export", command=self.query_and_export)
        self.query_button.pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=2, column=0, pady=5)

    def calculate_alarm_statistics(self, df):
        df_sorted = df.sort_values(['point_id', 'timestamp'])
        alarm_stats = []
        
        for point_id, group in df_sorted.groupby('point_id'):
            durations = []
            generation_time = None
            
            for _, row in group.iterrows():
                if row['_VAL'] == 'G':
                    generation_time = row['timestamp']
                elif row['_VAL'] == 'R' and generation_time is not None:
                    duration = (row['timestamp'] - generation_time).total_seconds() / 60
                    durations.append((row['timestamp'].date(), duration))
                    generation_time = None
            
            if durations:
                day_stats = {}
                for date, duration in durations:
                    if date not in day_stats:
                        day_stats[date] = []
                    day_stats[date].append(duration)
                
                for date, daily_durations in day_stats.items():
                    alarm_stats.append({
                        'point_id': point_id,
                        'date': date,
                        'avg_duration_minutes': round(sum(daily_durations) / len(daily_durations), 2),
                        'total_duration_minutes': round(sum(daily_durations), 2),
                        'occurrences': len(daily_durations),
                    })
        
        return pd.DataFrame(alarm_stats)

    def calculate_total_statistics(self, df):
        df_sorted = df.sort_values(['point_id', 'timestamp'])
        total_stats = []
        
        for point_id, group in df_sorted.groupby('point_id'):
            durations = []
            generation_time = None
            
            for _, row in group.iterrows():
                if row['_VAL'] == '1':
                    generation_time = row['timestamp']
                elif row['_VAL'] == '0' and generation_time is not None:
                    duration = (row['timestamp'] - generation_time).total_seconds() / 60
                    durations.append(duration)
                    generation_time = None
            
            if durations:
                total_stats.append({
                    'point_id': point_id,
                    'avg_duration_minutes': round(sum(durations) / len(durations), 2),
                    'total_duration_minutes': round(sum(durations), 2),
                    'total_occurrences': len(durations),
                })
        
        return pd.DataFrame(total_stats)

    def export_to_excel(self, df, stats_df, total_stats_df, file_path):
        def format_header(worksheet):
            for cell in worksheet[1]:
                cell.font = openpyxl.styles.Font(bold=True)
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = max_length + 2
                worksheet.column_dimensions[column].width = adjusted_width

        top_occurrences = total_stats_df.sort_values('total_occurrences', ascending=False).head(50)
        top_duration = total_stats_df.sort_values('total_duration_minutes', ascending=False).head(50)
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='RAW Data', index=False)
            if not stats_df.empty:
                stats_df.to_excel(writer, sheet_name='Daily Analysis', index=False)
            if not total_stats_df.empty:
                total_stats_df.to_excel(writer, sheet_name='Total Analysis', index=False)
                top_occurrences.to_excel(writer, sheet_name='Top Occurrences', index=False)
                top_duration.to_excel(writer, sheet_name='Top Duration', index=False)

            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                format_header(worksheet)

    def query_and_export(self):
        if not self.validate_dates():
            return
            
        self.query_button.state(['disabled'])
        self.progress_var.set("Querying database...")
        self.root.update_idletasks()
        
        try:
            start_date_str = f"{self.start_date.selection_get().strftime('%Y-%m-%d')} {self.start_hour.get()}:{self.start_minute.get()}:{self.start_second.get()}"
            end_date_str = f"{self.end_date.selection_get().strftime('%Y-%m-%d')} {self.end_hour.get()}:{self.end_minute.get()}:{self.end_second.get()}"
            
            # change report to view ALL alarms (not just singulator, cc, etc.)
            # query = """
            # SELECT 
            #     [timestamp], 
            #     [point_id],
            #     [_VAL]
            # FROM [CIMPLICITY].[dbo].[DATA_LOG]
            # WHERE [timestamp] BETWEEN ? AND ?
            # ORDER BY [timestamp] DESC
            # """

            query = """
            SELECT 
                [timestamp], 
                [point_id],
                [_VAL]
            FROM [CIMPLICITY].[dbo].[DATA_LOG]
            WHERE point_id LIKE 'CC%'
                AND [timestamp] BETWEEN ? AND ?
            ORDER BY [timestamp] DESC
            """

            with self.get_connection() as conn:
                df = pd.read_sql(query, conn, params=(start_date_str, end_date_str))
            
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            if df.empty:
                messagebox.showinfo("Info", "No data found for the selected date/time range.")
                return
                
            filename = f"alarm_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path = os.path.join(self.current_dir, filename)
            
            self.progress_var.set("Calculating alarm statistics...")
            self.root.update_idletasks()
            
            stats_df = self.calculate_alarm_statistics(df)
            total_stats_df = self.calculate_total_statistics(df)
            
            self.progress_var.set("Exporting to Excel...")
            self.root.update_idletasks()
            
            self.export_to_excel(df, stats_df, total_stats_df, file_path)
            
            self.progress_var.set(f"Export completed: {filename}")
            messagebox.showinfo("Success", f"Data exported to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.query_button.state(['!disabled'])
            
    def validate_dates(self):
        try:
            start_date = datetime.strptime(
                f"{self.start_date.selection_get().strftime('%Y-%m-%d')} {self.start_hour.get()}:{self.start_minute.get()}:{self.start_second.get()}",
                "%Y-%m-%d %H:%M:%S"
            )
            end_date = datetime.strptime(
                f"{self.end_date.selection_get().strftime('%Y-%m-%d')} {self.end_hour.get()}:{self.end_minute.get()}:{self.end_second.get()}",
                "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return False
        
        if start_date > end_date:
            messagebox.showerror("Error", "Start date/time must be before end date/time")
            return False
        
        return True

    def on_closing(self):
        if self.engine:
            self.engine.dispose()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseQueryApp(root)
    root.mainloop()
