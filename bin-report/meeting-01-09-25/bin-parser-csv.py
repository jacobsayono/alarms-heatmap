import pandas as pd
import numpy as np
import sys

# Hardcoded list of specific alarm IDs to process
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

# Read the Excel file
df = pd.read_excel(file_path)

# Format date-time and fill empty cells
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['point_val'] = df['point_val'].fillna(0).astype(int)

# Filter rows by the hardcoded list of alarm IDs
df = df[df['alarm_id'].isin(specific_alarms)]

# Sort by timestamp
df = df.sort_values(by='timestamp')

# Initialize data structures
total_time_differences = {}
trigger_counts = {}
active_triggers = {}

# Process each row
for _, row in df.iterrows():
    alarm_id = row['alarm_id']
    point_val = row['point_val']
    timestamp = row['timestamp']

    # Initialize alarm ID if not present
    if alarm_id not in trigger_counts:
        trigger_counts[alarm_id] = 0
        total_time_differences[alarm_id] = pd.Timedelta(0)
        active_triggers[alarm_id] = None

    if point_val == 1:
        # Start of a new alarm trigger
        trigger_counts[alarm_id] += 1
        active_triggers[alarm_id] = timestamp
    elif point_val == 0:
        # End of an alarm trigger
        if active_triggers[alarm_id] is not None:
            # Calculate time difference
            time_diff = timestamp - active_triggers[alarm_id]
            total_time_differences[alarm_id] += time_diff
            # Reset active trigger
            active_triggers[alarm_id] = None

# Ensure all alarms from the specific list are in the dictionary
for alarm_id in specific_alarms:
    if alarm_id not in total_time_differences:
        total_time_differences[alarm_id] = pd.Timedelta(0)
        trigger_counts[alarm_id] = 0

# Output results
results = pd.DataFrame({
    'alarm_id': list(trigger_counts.keys()),
    'trigger_count': list(trigger_counts.values()),
    # 'total_downtime': [str(total_time_differences[alarm]) for alarm in trigger_counts.keys()]
    'total_downtime': [int(total_time_differences[alarm].total_seconds()) for alarm in trigger_counts.keys()]
})

# Sort the results according to the specific_alarms list
results['sort_order'] = results['alarm_id'].apply(lambda x: specific_alarms.index(x))
results = results.sort_values(by='sort_order').drop(columns=['sort_order'])

# Export to CSV
output_file = "output.csv"
results.to_csv(output_file, index=False)

print(f"Results exported to {output_file}")
