import pandas as pd
import numpy as np
import sys

###############################################
# 1) USER-DEFINED CONFIG
###############################################

# (A) List of bin prefixes you want in the output.
#     Example: CC6.Bin_BRight, CC8.Bin_BLeft, etc.
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

# (B) The 3 suffixes we care about:
suffixes = ["_Full", "_NotPresent", "_PresentNotResumed"]

# (C) 24 hourly buckets starting at 07:00
#    (We assume we only want a single 24-hour window from 7:00.)
#    If our data has multiple days, we'll need to adapt or loop over days.
NUM_HOURS = 24

###############################################
# 2) HELPER FUNCTIONS
###############################################

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

###############################################
# 3) MAIN SCRIPT
###############################################

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [filename.xlsx]")
        sys.exit(1)

    file_path = sys.argv[1]
    df = pd.read_excel(file_path)

    # Convert timestamps, fill NAs, etc.
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['_VAL'] = df['_VAL'].fillna(0).astype(int)

    # --------------------------------
    # A) Build a full list of point_ids we care about.
    #    For each prefix, we have 3 sub-alarms (Full, NotPresent, PresentNotResumed).
    # --------------------------------
    all_alarms = []
    prefix_to_sub_alarms = {}
    for prefix in prefix_list:
        sub_alarms = [prefix + sfx for sfx in suffixes]
        prefix_to_sub_alarms[prefix] = sub_alarms
        all_alarms.extend(sub_alarms)
    
    # Filter DF to only those point_ids
    df = df[df['point_id'].isin(all_alarms)]
    
    # Sort by timestamp
    df = df.sort_values(by='timestamp')

    # --------------------------------
    # B) Define 24 hourly intervals, starting from earliest day at 07:00
    #    (We do a single day example: from day_start=07:00 to day_start+24h.)
    # --------------------------------
    min_date = df['timestamp'].min().floor('D')
    start_of_day = min_date.replace(hour=7, minute=0, second=0, microsecond=0)
    
    hourly_intervals = []
    current = start_of_day
    for i in range(NUM_HOURS):
        next_hour = current + pd.Timedelta(hours=1)
        hourly_intervals.append((current, next_hour))
        current = next_hour
    
    # For naming the columns, we'll use "07:00", "08:00", etc.
    def format_hour_label(ts):
        return ts.strftime('%H:%M')
    
    interval_labels = [format_hour_label(s) for (s, e) in hourly_intervals]
    count_cols = [lbl + "_count" for lbl in interval_labels]
    downtime_cols = [lbl + "_downtime" for lbl in interval_labels]

    # --------------------------------
    # C) For each prefix, build intervals for the 3 suffix alarms,
    #    sum their downtime, but only count triggers from the _Full intervals.
    # --------------------------------
    
    #  We'll store data as:
    #     alarm_hour_data[prefix][hour_index] = [downtime_seconds, trigger_count]
    #  Then convert to DataFrame at the end.
    alarm_hour_data = {
        prefix: {i: [0.0, 0] for i in range(NUM_HOURS)}
        for prefix in prefix_list
    }

    # Helper function to add intervals into the "alarm_hour_data[prefix]"
    def accumulate_intervals(prefix, intervals, add_triggers=False):
        """
        prefix: e.g. 'CC6.Bin_BRight'
        intervals: list of (start_ts, end_ts) for that alarm
        add_triggers: if True, we add 'trigger_count' from these intervals
        """
        # We only consider overlap in [hour0_start, hourN_end]
        day_start = hourly_intervals[0][0]
        day_end = hourly_intervals[-1][1]  # 7:00 next day
        
        for (start_ts, end_ts) in intervals:
            # Skip if no overlap
            if end_ts <= day_start or start_ts >= day_end:
                continue
            
            st = max(start_ts, day_start)
            en = min(end_ts, day_end)
            
            bucket_dict = split_into_hourly_buckets(st, en, hourly_intervals)
            
            for i in range(NUM_HOURS):
                # downtime
                alarm_hour_data[prefix][i][0] += bucket_dict[i][0]
                # triggers
                # Only add trigger if add_triggers = True
                if add_triggers:
                    alarm_hour_data[prefix][i][1] += bucket_dict[i][1]

    # Process each prefix
    for prefix in prefix_list:
        sub_alarms = prefix_to_sub_alarms[prefix]
        # We expect sub_alarms = [prefix+"_Full", prefix+"_NotPresent", prefix+"_PresentNotResumed"]

        # 1) Build intervals for each sub alarm
        #    We'll store them in a dictionary sfx -> [(start_ts, end_ts), ...]
        intervals_map = {}
        for point_id in sub_alarms:
            # Filter df for just this point_id
            df_sub = df[df['point_id'] == point_id]
            if df_sub.empty:
                intervals_map[point_id] = []
                continue
            intervals_map[point_id] = build_intervals_per_alarm(df_sub)

        # 2) Accumulate the downtime from all 3 suffix alarms
        #    i.e. we sum up durations for _Full, _NotPresent, _PresentNotResumed
        #    But the trigger counts only come from the "_Full" intervals.
        for point_id in sub_alarms:
            add_trigs = True if point_id.endswith("_Full") else False
            intervals = intervals_map[point_id]
            accumulate_intervals(prefix, intervals, add_triggers=add_trigs)
    
    # --------------------------------
    # D) Build final DataFrame
    # --------------------------------
    rows = []
    for prefix in prefix_list:
        row_dict = {"point_id": prefix}
        for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
            sec = alarm_hour_data[prefix][i][0]  # total downtime seconds
            trig = alarm_hour_data[prefix][i][1] # trigger count
            row_dict[count_cols[i]] = trig
            row_dict[downtime_cols[i]] = sec
        rows.append(row_dict)
    
    results = pd.DataFrame(rows)

    # Sort by the order of prefix_list
    results['sort_order'] = results['point_id'].apply(lambda x: prefix_list.index(x))
    results = results.sort_values('sort_order').drop(columns=['sort_order'])

    # --------------------------------
    # E) Export separate CSVs: triggers vs. downtime
    # --------------------------------
    # (1) Trigger counts only
    results_counts = results[['point_id'] + count_cols].copy()
    rename_map_counts = {col: col.replace("_count", "") for col in count_cols}
    results_counts = results_counts.rename(columns=rename_map_counts)
    results_counts.to_csv("hourly-trigger.csv", index=False)
    print("Hourly trigger counts exported to hourly-trigger.csv")

    # (2) Downtime only
    results_downtime = results[['point_id'] + downtime_cols].copy()
    rename_map_downtime = {col: col.replace("_downtime", "") for col in downtime_cols}
    results_downtime = results_downtime.rename(columns=rename_map_downtime)
    results_downtime.to_csv("hourly-downtime.csv", index=False)
    print("Hourly downtime exported to hourly-downtime.csv")


if __name__ == "__main__":
    main()
