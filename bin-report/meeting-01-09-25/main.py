import pandas as pd
import numpy as np
import sys

# Hardcoded list of specific alarm IDs to process (same as your code)
specific_alarms = [
    "CC6.Bin_BRight_Full",
    "CC7.Bin_BRight_Full",
    "CC8.Bin_BLeft_Full",
    "CC8.Bin_BRight_Full",
    "CC9.Bin_BRight_Full",
    "CC10.Bin_BLeft_Full",
    "CC10.Bin_BRight_Full",
    "CC11.Bin_BRight_Full",
    "CC12.Bin_BLeft_Full",
    "CC12.Bin_BRight_Full",
    "CC13.Bin_BRight_Full",
    "CC14.Bin_BLeft_Full",
    "CC14.Bin_BRight_Full",
    "CC15.Bin_BRight_Full",
    "CC16.Bin_BLeft_Full",
    "CC16.Bin_BRight_Full",
    "CC17.Bin_BRight_Full",
    "CC18.Bin_BLeft_Full",
    "CC18.Bin_BRight_Full",
    "CC19.Bin_BRight_Full",
    "CC20.Bin_BLeft_Full",
    "CC20.Bin_BRight_Full",
    "CC21.Bin_BRight_Full",
    "CC22.Bin_BLeft_Full",
    "CC22.Bin_BRight_Full",
    "CC23.Bin_BRight_Full",
    "CC24.Bin_BLeft_Full",
    "CC24.Bin_BRight_Full",
    "CC25.Bin_BRight_Full",
    "CC26.Bin_BLeft_Full",
    "CC26.Bin_BRight_Full",
    "CC27.Bin_BRight_Full",
    "CC28.Bin_BLeft_Full",
    "CC28.Bin_BRight_Full",
    "CC29.Bin_BRight_Full",
    "CC30.Bin_BLeft_Full",
    "CC30.Bin_BRight_Full",
    "CC31.Bin_BRight_Full",
    "CC32.Bin_BLeft_Full",
    "CC32.Bin_BRight_Full",
    "CC36.Bin_BLeft_Full",
    "CC36.Bin_BRight_Full",
    "CC37.Bin_BRight_Full",
    "CC38.Bin_BLeft_Full",
    "CC38.Bin_BRight_Full",
    "CC39.Bin_BRight_Full",
    "CC40.Bin_BLeft_Full",
    "CC40.Bin_BRight_Full",
    "CC41.Bin_BRight_Full",
    "CC42.Bin_BLeft_Full",
    "CC42.Bin_BRight_Full",
    "CC43.Bin_BRight_Full",
    "CC44.Bin_BLeft_Full",
    "CC44.Bin_BRight_Full",
    "CC45.Bin_BRight_Full",
    "CC46.Bin_BLeft_Full",
    "CC46.Bin_BRight_Full",
    "CC47.Bin_BRight_Full",
    "CC48.Bin_BLeft_Full",
    "CC48.Bin_BRight_Full",
    "CC49.Bin_BRight_Full",
    "CC50.Bin_BLeft_Full",
    "CC50.Bin_BRight_Full",
    "CC51.Bin_BRight_Full",
    "CC52.Bin_BLeft_Full",
    "CC52.Bin_BRight_Full",
    "CC53.Bin_BRight_Full",
    "CC54.Bin_BLeft_Full",
    "CC54.Bin_BRight_Full",
    "CC55.Bin_BRight_Full",
    "CC56.Bin_BLeft_Full",
    "CC56.Bin_BRight_Full",
    "CC57.Bin_BRight_Full",
    "CC58.Bin_BLeft_Full",
    "CC58.Bin_BRight_Full",
    "CC59.Bin_BRight_Full",
    "CC60.Bin_BLeft_Full",
    "CC60.Bin_BRight_Full",
    "CC61.Bin_BRight_Full",
    "CC62.Bin_BLeft_Full",
    "CC62.Bin_BRight_Full",
    "CC63.Bin_BRight_Full",
    "CC64.Bin_BLeft_Full",
    "CC64.Bin_BRight_Full",
    "CC65.Bin_BRight_Full",
    "CC66.Bin_BLeft_Full",
    "CC66.Bin_BRight_Full",
    "CC67.Bin_BRight_Full",
    "CC68.Bin_BLeft_Full",
    "CC68.Bin_BRight_Full",
    "CC69.Bin_BRight_Full",
    "CC70.Bin_BLeft_Full",
    "CC70.Bin_BRight_Full",
    "CC71.Bin_BRight_Full",
    "CC72.Bin_BLeft_Full",
    "CC72.Bin_BRight_Full",
    "CC73.Bin_BRight_Full",
    "CC74.Bin_BLeft_Full",
    "CC74.Bin_BRight_Full",
    "CC75.Bin_BRight_Full",
    "CC76.Bin_BLeft_Full",
    "CC76.Bin_BRight_Full",
    "CC77.Bin_BRight_Full"
]

# Check for the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python3 script.py [filename.xlsx]")
    sys.exit(1)

file_path = sys.argv[1]

# 1) Read the Excel file
df = pd.read_excel(file_path)

# 2) Format and filter
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['point_val'] = df['point_val'].fillna(0).astype(int)
df = df[df['alarm_id'].isin(specific_alarms)]
df = df.sort_values(by='timestamp')

# --------------------
# BUILD ALARM INTERVALS
# --------------------
alarm_intervals = {alarm_id: [] for alarm_id in specific_alarms}
active_start = {alarm_id: None for alarm_id in specific_alarms}

for _, row in df.iterrows():
    alarm_id = row['alarm_id']
    point_val = row['point_val']
    timestamp = row['timestamp']
    
    if point_val == 1:
        # Start of an alarm
        active_start[alarm_id] = timestamp
    else:
        # End of an alarm
        if active_start[alarm_id] is not None:
            interval = (active_start[alarm_id], timestamp)
            alarm_intervals[alarm_id].append(interval)
            active_start[alarm_id] = None

# ----------------------
# DEFINE THE 24 HOURLY BUCKETS
# ----------------------
min_date = df['timestamp'].min().floor('D')
start_of_day = min_date.replace(hour=7, minute=0, second=0, microsecond=0)

hourly_intervals = []
current = start_of_day
for i in range(24):
    next_hour = current + pd.Timedelta(hours=1)
    hourly_intervals.append((current, next_hour))
    current = next_hour

def format_hour_label(start_ts, end_ts):
    # return f"{start_ts.strftime('%H:%M')}_{end_ts.strftime('%H:%M')}"
    return f"{start_ts.strftime('%H:%M')}"

interval_labels = [format_hour_label(s, e) for (s,e) in hourly_intervals]

count_cols = [lbl+"_count" for lbl in interval_labels]
downtime_cols = [lbl+"_downtime" for lbl in interval_labels]

# ----------------------
# FUNCTION TO SPLIT AN INTERVAL INTO HOUR BUCKETS
# ----------------------
def split_into_hourly_buckets(start_time, end_time):
    """
    Return a dict {bucket_index: (downtime_seconds, trigger_count)}
    """
    bucket_data = {i: [0.0, 0] for i in range(24)}
    
    for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
        overlap_start = max(start_time, bucket_start)
        overlap_end   = min(end_time, bucket_end)
        
        if overlap_end > overlap_start:
            overlap_seconds = (overlap_end - overlap_start).total_seconds()
            bucket_data[i][0] += overlap_seconds  # downtime
            
            # If the alarm started in this bucket, increment trigger count
            if start_time >= bucket_start and start_time < bucket_end:
                bucket_data[i][1] += 1
    
    return bucket_data

# ----------------------
# ACCUMULATE PER-ALARM, PER-HOUR
# ----------------------
alarm_hour_data = {
    alarm_id: {i: [0.0, 0] for i in range(24)}
    for alarm_id in specific_alarms
}

for alarm_id in specific_alarms:
    intervals = alarm_intervals[alarm_id]
    
    for (start_ts, end_ts) in intervals:
        day_start = hourly_intervals[0][0]   # 07:00
        day_end   = hourly_intervals[-1][1]  # next day 07:00
        
        # Skip intervals that don't overlap
        if end_ts < day_start or start_ts >= day_end:
            continue
        
        st = max(start_ts, day_start)
        en = min(end_ts, day_end)
        
        bucket_dict = split_into_hourly_buckets(st, en)
        
        for i in range(24):
            alarm_hour_data[alarm_id][i][0] += bucket_dict[i][0]  # downtime seconds
            alarm_hour_data[alarm_id][i][1] += bucket_dict[i][1]  # trigger count

# ----------------------
# BUILD FINAL TABLE
# ----------------------
rows = []
for alarm_id in specific_alarms:
    row_dict = {"alarm_id": alarm_id}
    for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
        sec = alarm_hour_data[alarm_id][i][0]  # downtime seconds
        trig = alarm_hour_data[alarm_id][i][1] # triggers
        row_dict[count_cols[i]] = trig
        row_dict[downtime_cols[i]] = sec
    rows.append(row_dict)

results = pd.DataFrame(rows)

# Sort according to your specific_alarms list
results['sort_order'] = results['alarm_id'].apply(lambda x: specific_alarms.index(x))
results = results.sort_values(by='sort_order').drop(columns=['sort_order'])

# ----------------------
# SPLIT INTO TWO SEPARATE DATAFRAMES & EXPORT
# ----------------------
# 1) Trigger counts only
results_counts = results[['alarm_id'] + count_cols].copy()
rename_map_counts = {
    col: col.replace("_count", "")
    for col in count_cols
}
results_counts = results_counts.rename(columns=rename_map_counts)

results_counts.to_csv("hourly-count.csv", index=False)
print("Hourly trigger counts exported to hourly-count.csv")

# 2) Downtime only
results_downtime = results[['alarm_id'] + downtime_cols].copy()
rename_map_downtime = {
    col: col.replace("_downtime", "")
    for col in downtime_cols
}
results_downtime = results_downtime.rename(columns=rename_map_downtime)

results_downtime.to_csv("hourly-downtime.csv", index=False)
print("Hourly downtime exported to hourly-downtime.csv")
