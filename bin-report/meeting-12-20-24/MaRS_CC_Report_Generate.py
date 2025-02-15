import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
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

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        date_frame = ttk.LabelFrame(main_frame, text="Date Range", padding=10)
        date_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        start_frame = ttk.Frame(date_frame)
        start_frame.grid(row=0, column=0, padx=5)
        ttk.Label(start_frame, text="Start Date:").grid(row=0, column=0, pady=5)
        self.start_date = Calendar(start_frame, selectmode='day', date_pattern='y-mm-dd')
        self.start_date.grid(row=1, column=0)
        
        end_frame = ttk.Frame(date_frame)
        end_frame.grid(row=0, column=1, padx=5)
        ttk.Label(end_frame, text="End Date:").grid(row=0, column=0, pady=5)
        self.end_date = Calendar(end_frame, selectmode='day', date_pattern='y-mm-dd')
        self.end_date.grid(row=1, column=0)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        self.query_button = ttk.Button(button_frame, text="Run Query & Export", command=self.query_and_export)
        self.query_button.pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.StringVar()
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=2, column=0, pady=5)

    def calculate_alarm_statistics(self, df):
        df_sorted = df.sort_values(['alarm_id', 'timestamp'])
        alarm_stats = []
        
        for alarm_id, group in df_sorted.groupby('alarm_id'):
            durations = []
            timestamp_date = None
            generation_time = None
            
            for _, row in group.iterrows():
                date = row['timestamp'].date()
                
                if row['log_action'] == 'G':
                    generation_time = row['timestamp']
                elif row['log_action'] == 'R' and generation_time is not None:
                    duration = (row['timestamp'] - generation_time).total_seconds() / 60
                    durations.append((date, duration))
                    generation_time = None
            
            if durations:
                day_stats = {}
                for date, duration in durations:
                    if date not in day_stats:
                        day_stats[date] = []
                    day_stats[date].append(duration)
                
                for date, daily_durations in day_stats.items():
                    alarm_stats.append({
                        'alarm_id': alarm_id,
                        'date': date,
                        'avg_duration_minutes': round(sum(daily_durations) / len(daily_durations), 2),
                        'total_duration_minutes': round(sum(daily_durations), 2),
                        'occurrences': len(daily_durations),
                        'alarm_message': group['alarm_message'].iloc[0]
                    })
        
        return pd.DataFrame(alarm_stats)

    def calculate_total_statistics(self, df):
        df_sorted = df.sort_values(['alarm_id', 'timestamp'])
        total_stats = []
        
        for alarm_id, group in df_sorted.groupby('alarm_id'):
            durations = []
            generation_time = None
            
            for _, row in group.iterrows():
                if row['log_action'] == 'G':
                    generation_time = row['timestamp']
                elif row['log_action'] == 'R' and generation_time is not None:
                    duration = (row['timestamp'] - generation_time).total_seconds() / 60
                    durations.append(duration)
                    generation_time = None
            
            if durations:
                total_stats.append({
                    'alarm_id': alarm_id,
                    'avg_duration_minutes': round(sum(durations) / len(durations), 2),
                    'total_duration_minutes': round(sum(durations), 2),
                    'total_occurrences': len(durations),
                    'alarm_message': group['alarm_message'].iloc[0]
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
            # Export all sheets
            df.to_excel(writer, sheet_name='RAW Data', index=False)
            if not stats_df.empty:
                stats_df.to_excel(writer, sheet_name='Daily Analysis', index=False)
            if not total_stats_df.empty:
                total_stats_df.to_excel(writer, sheet_name='Total Analysis', index=False)
                top_occurrences.to_excel(writer, sheet_name='Top Occurrences', index=False)
                top_duration.to_excel(writer, sheet_name='Top Duration', index=False)
            
            # Format each sheet
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
            start_date = self.start_date.selection_get().strftime('%Y-%m-%d 00:00:00')
            end_date = self.end_date.selection_get().strftime('%Y-%m-%d 23:59:59')
            
            query = """
            SELECT 
                [timestamp], 
                [alarm_id], 
                [point_val], 
                [alarm_message],
                [log_action]
            FROM [CIMPLICITY].[dbo].[ALARM_LOG]
            WHERE alarm_id LIKE 'CC%'
                AND [timestamp] BETWEEN ? AND ?
            ORDER BY [timestamp] DESC
            """
            
            with self.get_connection() as conn:
                df = pd.read_sql(query, conn, params=(start_date, end_date))
            
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            if df.empty:
                messagebox.showinfo("Info", "No data found for the selected date range")
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
        start = self.start_date.selection_get()
        end = self.end_date.selection_get()
        
        if start > end:
            messagebox.showerror("Error", "Start date must be before end date")
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