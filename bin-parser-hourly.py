import pandas as pd
import numpy as np
import sys

# Hardcoded list of specific alarm IDs to process (same as your code)
specific_alarms = [
    "CC1.Bin_BLeft_Full",
    "CC1.Bin_BRight_Full",
    "CC2.Bin_BLeft_Full",
    "CC2.Bin_BRight_Full",
    "CC3.Bin_BLeft_Full",
    "CC3.Bin_BRight_Full",
    "CC4.Bin_BLeft_Full",
    "CC4.Bin_BRight_Full",
    "CC5.Bin_BLeft_Full",
    "CC5.Bin_BRight_Full",
    "CC6.Bin_BLeft_Full",
    "CC6.Bin_BRight_Full",
    "CC7.Bin_BLeft_Full",
    "CC7.Bin_BRight_Full",
    "CC8.Bin_BLeft_Full",
    "CC8.Bin_BRight_Full",
    "CC9.Bin_BLeft_Full",
    "CC9.Bin_BRight_Full",
    "CC10.Bin_BLeft_Full",
    "CC10.Bin_BRight_Full",
    "CC11.Bin_BLeft_Full",
    "CC11.Bin_BRight_Full",
    "CC12.Bin_BLeft_Full",
    "CC12.Bin_BRight_Full",
    "CC13.Bin_BLeft_Full",
    "CC13.Bin_BRight_Full",
    "CC14.Bin_BLeft_Full",
    "CC14.Bin_BRight_Full",
    "CC15.Bin_BLeft_Full",
    "CC15.Bin_BRight_Full",
    "CC16.Bin_BLeft_Full",
    "CC16.Bin_BRight_Full",
    "CC17.Bin_BLeft_Full",
    "CC17.Bin_BRight_Full",
    "CC18.Bin_BLeft_Full",
    "CC18.Bin_BRight_Full",
    "CC19.Bin_BLeft_Full",
    "CC19.Bin_BRight_Full",
    "CC20.Bin_BLeft_Full",
    "CC20.Bin_BRight_Full",
    "CC21.Bin_BLeft_Full",
    "CC21.Bin_BRight_Full",
    "CC22.Bin_BLeft_Full",
    "CC22.Bin_BRight_Full",
    "CC23.Bin_BLeft_Full",
    "CC23.Bin_BRight_Full",
    "CC24.Bin_BLeft_Full",
    "CC24.Bin_BRight_Full",
    "CC25.Bin_BLeft_Full",
    "CC25.Bin_BRight_Full",
    "CC26.Bin_BLeft_Full",
    "CC26.Bin_BRight_Full",
    "CC27.Bin_BLeft_Full",
    "CC27.Bin_BRight_Full",
    "CC28.Bin_BLeft_Full",
    "CC28.Bin_BRight_Full",
    "CC29.Bin_BLeft_Full",
    "CC29.Bin_BRight_Full",
    "CC30.Bin_BLeft_Full",
    "CC30.Bin_BRight_Full",
    "CC31.Bin_BLeft_Full",
    "CC31.Bin_BRight_Full",
    "CC32.Bin_BLeft_Full",
    "CC32.Bin_BRight_Full",
    "CC33.Bin_BLeft_Full",
    "CC33.Bin_BRight_Full",
    "CC34.Bin_BLeft_Full",
    "CC34.Bin_BRight_Full",
    "CC35.Bin_BLeft_Full",
    "CC35.Bin_BRight_Full",
    "CC36.Bin_BLeft_Full",
    "CC36.Bin_BRight_Full",
    "CC37.Bin_BLeft_Full",
    "CC37.Bin_BRight_Full",
    "CC38.Bin_BLeft_Full",
    "CC38.Bin_BRight_Full",
    "CC39.Bin_BLeft_Full",
    "CC39.Bin_BRight_Full",
    "CC40.Bin_BLeft_Full",
    "CC40.Bin_BRight_Full",
    "CC41.Bin_BLeft_Full",
    "CC41.Bin_BRight_Full",
    "CC42.Bin_BLeft_Full",
    "CC42.Bin_BRight_Full",
    "CC43.Bin_BLeft_Full",
    "CC43.Bin_BRight_Full",
    "CC44.Bin_BLeft_Full",
    "CC44.Bin_BRight_Full",
    "CC45.Bin_BLeft_Full",
    "CC45.Bin_BRight_Full",
    "CC46.Bin_BLeft_Full",
    "CC46.Bin_BRight_Full",
    "CC47.Bin_BLeft_Full",
    "CC47.Bin_BRight_Full",
    "CC48.Bin_BLeft_Full",
    "CC48.Bin_BRight_Full",
    "CC49.Bin_BLeft_Full",
    "CC49.Bin_BRight_Full",
    "CC50.Bin_BLeft_Full",
    "CC50.Bin_BRight_Full",
    "CC51.Bin_BLeft_Full",
    "CC51.Bin_BRight_Full",
    "CC52.Bin_BLeft_Full",
    "CC52.Bin_BRight_Full",
    "CC53.Bin_BLeft_Full",
    "CC53.Bin_BRight_Full",
    "CC54.Bin_BLeft_Full",
    "CC54.Bin_BRight_Full",
    "CC55.Bin_BLeft_Full",
    "CC55.Bin_BRight_Full",
    "CC56.Bin_BLeft_Full",
    "CC56.Bin_BRight_Full",
    "CC57.Bin_BLeft_Full",
    "CC57.Bin_BRight_Full",
    "CC58.Bin_BLeft_Full",
    "CC58.Bin_BRight_Full",
    "CC59.Bin_BLeft_Full",
    "CC59.Bin_BRight_Full",
    "CC60.Bin_BLeft_Full",
    "CC60.Bin_BRight_Full",
    "CC61.Bin_BLeft_Full",
    "CC61.Bin_BRight_Full",
    "CC62.Bin_BLeft_Full",
    "CC62.Bin_BRight_Full",
    "CC63.Bin_BLeft_Full",
    "CC63.Bin_BRight_Full",
    "CC64.Bin_BLeft_Full",
    "CC64.Bin_BRight_Full",
    "CC65.Bin_BLeft_Full",
    "CC65.Bin_BRight_Full",
    "CC66.Bin_BLeft_Full",
    "CC66.Bin_BRight_Full",
    "CC67.Bin_BLeft_Full",
    "CC67.Bin_BRight_Full",
    "CC68.Bin_BLeft_Full",
    "CC68.Bin_BRight_Full",
    "CC69.Bin_BLeft_Full",
    "CC69.Bin_BRight_Full",
    "CC70.Bin_BLeft_Full",
    "CC70.Bin_BRight_Full",
    "CC71.Bin_BLeft_Full",
    "CC71.Bin_BRight_Full",
    "CC72.Bin_BLeft_Full",
    "CC72.Bin_BRight_Full",
    "CC73.Bin_BLeft_Full",
    "CC73.Bin_BRight_Full",
    "CC74.Bin_BLeft_Full",
    "CC74.Bin_BRight_Full",
    "CC75.Bin_BLeft_Full",
    "CC75.Bin_BRight_Full",
    "CC76.Bin_BLeft_Full",
    "CC76.Bin_BRight_Full",
    "CC77.Bin_BLeft_Full",
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
# We'll collect start/end pairs for each alarm in a dictionary:
#   alarm_intervals[alarm_id] = [ (start_time, end_time), (start_time, end_time), ... ]
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
            # We have a valid start -> end pair
            interval = (active_start[alarm_id], timestamp)
            alarm_intervals[alarm_id].append(interval)
            # Reset
            active_start[alarm_id] = None

# If some alarms never ended by the last row in the data,
# you can decide whether you want to "close" them at the last timestamp in the dataset
# or ignore them. For daily reporting, you might do something like:
# for alarm_id in specific_alarms:
#     if active_start[alarm_id] is not None:
#         # close at last timestamp
#         last_ts = df['timestamp'].max()
#         alarm_intervals[alarm_id].append((active_start[alarm_id], last_ts))
#         active_start[alarm_id] = None

# ----------------------
# DEFINE THE 24 HOURLY BUCKETS
# ----------------------
# You likely have data covering multiple days, but let's assume we want
# a single "day" from 07:00 to the next day's 06:00 with 24 buckets.
#
# We'll pick the *start* day from the min of all timestamps' date, but
# you can hardcode the date if you wish.
#
# The key is: intervals:
#   [07:00, 08:00),
#   [08:00, 09:00),
#   ...
#   [05:00, 06:00),
#   [06:00, 07:00)  (the next day)
#

min_date = df['timestamp'].min().floor('D')  # e.g. 2024-12-15 00:00:00
# Force the "start" to be that date plus 07:00
start_of_day = min_date.replace(hour=7, minute=0, second=0, microsecond=0)

# Build the 24 intervals from 07:00 to next-day 06:00
hourly_intervals = []
current = start_of_day
for i in range(24):
    # next hour
    next_hour = current + pd.Timedelta(hours=1)
    hourly_intervals.append((current, next_hour))
    current = next_hour

# That yields: [ (07:00, 08:00), (08:00, 09:00), ..., (06:00, 07:00) next day ]

# For convenience, let's create some labels for columns:
# e.g. "07:00_08:00_count" and "07:00_08:00_downtime"
def format_hour_label(start_ts, end_ts):
    return f"{start_ts.strftime('%H:%M')}_{end_ts.strftime('%H:%M')}"

interval_labels = [format_hour_label(s, e) for (s,e) in hourly_intervals]

# We'll create "count" columns and "downtime" columns
count_cols = [lbl+"_count" for lbl in interval_labels]
downtime_cols = [lbl+"_downtime" for lbl in interval_labels]

# ----------------------
# FUNCTION TO SPLIT AN INTERVAL INTO HOUR BUCKETS
# ----------------------
def split_into_hourly_buckets(start_time, end_time):
    """
    Return a dict {bucket_index: (downtime_seconds, trigger_count)}
    where bucket_index is 0..23 for each of the 24 intervals.
    
    - We only increment the trigger count in the bucket in which the 'start_time' falls.
    - We accumulate downtime in whichever buckets the alarm spans (split by boundaries).
    """
    # results dict (bucket -> [downtime_in_seconds, trigger_count])
    bucket_data = {i: [0.0, 0] for i in range(24)}
    
    # Figure out which hourly bucket the alarm STARTS in, so we can set trigger_count=1 there
    # If it starts before 07:00, it effectively enters the "0th" bucket at 07:00.
    
    for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
        # Find the overlap between (start_time, end_time) and (bucket_start, bucket_end)
        overlap_start = max(start_time, bucket_start)
        overlap_end   = min(end_time, bucket_end)
        
        if overlap_end > overlap_start:
            # There's a positive overlap
            overlap_seconds = (overlap_end - overlap_start).total_seconds()
            bucket_data[i][0] += overlap_seconds  # downtime in seconds
            
            # If the alarm started in this bucket, add 1 to the trigger count
            # i.e. if start_time is in [bucket_start, bucket_end)
            if start_time >= bucket_start and start_time < bucket_end:
                bucket_data[i][1] += 1
    
    return bucket_data

# ----------------------
# ACCUMULATE PER-ALARM, PER-HOUR
# ----------------------
# We'll end up with a structure: alarm_hour_data[alarm_id][i] = (total downtime in sec, total triggers)
alarm_hour_data = {
    alarm_id: {i: [0.0, 0] for i in range(24)}
    for alarm_id in specific_alarms
}

for alarm_id in specific_alarms:
    intervals = alarm_intervals[alarm_id]  # list of (start, end) for this alarm
    
    for (start_ts, end_ts) in intervals:
        # Clip to the overall 24-hour window if desired
        # If the data might be beyond the 07:00->06:00 next day, you can clip.
        # For example:
        day_start = hourly_intervals[0][0]   # 07:00
        day_end   = hourly_intervals[-1][1]  # next day 07:00
        if end_ts < day_start or start_ts >= day_end:
            # no overlap with this day
            continue
        
        # Optionally clamp to [day_start, day_end)
        st = max(start_ts, day_start)
        en = min(end_ts, day_end)
        
        # Get this interval's split
        bucket_dict = split_into_hourly_buckets(st, en)
        
        # Add them to alarm_hour_data
        for i in range(24):
            alarm_hour_data[alarm_id][i][0] += bucket_dict[i][0]  # downtime seconds
            alarm_hour_data[alarm_id][i][1] += bucket_dict[i][1]  # trigger count

# ----------------------
# BUILD FINAL TABLE
# ----------------------
# We want columns for alarm_id + 24 "count" columns + 24 "downtime" columns
rows = []
for alarm_id in specific_alarms:
    row_dict = {"alarm_id": alarm_id}
    for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
        sec = alarm_hour_data[alarm_id][i][0]  # total downtime in seconds
        trig = alarm_hour_data[alarm_id][i][1] # total triggers
        row_dict[count_cols[i]] = trig
        # convert downtime to a string "HH:MM:SS" or a Timedelta if you prefer
        td = pd.Timedelta(seconds=sec)
        row_dict[downtime_cols[i]] = str(td)
    rows.append(row_dict)

results = pd.DataFrame(rows)

# Sort the results according to your specific_alarms list (so the final CSV is in the same order)
results['sort_order'] = results['alarm_id'].apply(lambda x: specific_alarms.index(x))
results = results.sort_values(by='sort_order').drop(columns=['sort_order'])

# Finally, export to CSV
output_file = "output_by_hour.csv"
results.to_csv(output_file, index=False)

print(f"Hourly results exported to {output_file}")
