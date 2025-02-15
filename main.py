import pandas as pd
import sys

# terminal input argument
if len(sys.argv) != 2:
    print("Usage: python3 script.py [filename.xlsx]")
    sys.exit(1)

file_path = sys.argv[1]

# load file
df = pd.read_excel(file_path)

# format date-time and fill empty cells
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['point_val'] = df['point_val'].fillna(0).astype(int)

# sort by timestamp
df = df.sort_values(by='timestamp')

# init dictionaries for total time differences and trigger counts
total_time_differences = {}
trigger_counts = {}

# iter thru rows to process log data
for _, row in df.iterrows():
    alarm_id = row['alarm_id']
    point_val = row['point_val']
    timestamp = row['timestamp']
    
    # init trigger time if it's first time seeing this alarm_id
    if alarm_id not in trigger_counts:
        trigger_counts[alarm_id] = 0
        total_time_differences[alarm_id] = pd.Timedelta(0)
    
    # when a trigger is encountered (point_val = 1)
    if point_val == 1:
        trigger_counts[alarm_id] += 1
        trigger_time = timestamp
    # when a resolution is encountered (point_val = 0)
    elif point_val == 0 and alarm_id in trigger_counts:
        # only process if there was a trigger before this resolution
        if trigger_counts[alarm_id] > 0:
            time_diff = timestamp - trigger_time  # calc time difference
            total_time_differences[alarm_id] += time_diff  # add to total time

# # sort total time differences by alarm_id alpha-numerically
# total_time_differences = dict(sorted(total_time_differences.items()))
# # sort trigger counts by alarm_id alpha-numerically
# trigger_counts = dict(sorted(trigger_counts.items()))

# sort total time differences by time difference (highest to lowest)
total_time_differences = dict(sorted(total_time_differences.items(), key=lambda item: item[1], reverse=True))
# sort trigger counts by trigger counts (highest to lowest)
trigger_counts = dict(sorted(trigger_counts.items(), key=lambda item: item[1], reverse=True))

# display total time differences in HH:MM:SS format
print("Total Downtime:")
for alarm_id, total_time in total_time_differences.items():
    # hours, remainder = divmod(total_time.seconds, 3600)
    # minutes, seconds = divmod(remainder, 60)
    # formatted_total_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    # print(f"{alarm_id}: {formatted_total_time}")
    print(f"{alarm_id}: {total_time}")

# display trigger counts
print("\nTrigger Counts:")
for alarm_id, trigger_count in trigger_counts.items():
    # print(f"{alarm_id}")
    print(f"{alarm_id}: {trigger_count}")
