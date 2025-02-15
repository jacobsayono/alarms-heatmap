import pandas as pd
import numpy as np
import sys

prefix_list_B = [
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

# prefix_list_A = [p.replace("Bin_B", "Bin_A") for p in prefix_list_B]

prefix_list_A = [
    "CC5.Bin_ARight",
    "CC6.Bin_ARight",
    "CC7.Bin_ARight",
    "CC8.Bin_ALeft",
    "CC8.Bin_ARight",
    "CC9.Bin_ARight",
    "CC10.Bin_ALeft",
    "CC10.Bin_ARight",
    "CC11.Bin_ARight",
    "CC12.Bin_ALeft",
    "CC12.Bin_ARight",
    "CC13.Bin_ARight",
    "CC14.Bin_ALeft",
    "CC14.Bin_ARight",
    "CC15.Bin_ARight",
    "CC16.Bin_ALeft",
    "CC16.Bin_ARight",
    "CC17.Bin_ARight",
    "CC18.Bin_ALeft",
    "CC18.Bin_ARight",
    "CC19.Bin_ARight",
    "CC20.Bin_ALeft",
    "CC20.Bin_ARight",
    "CC21.Bin_ARight",
    "CC22.Bin_ALeft",
    "CC22.Bin_ARight",
    "CC23.Bin_ARight",
    "CC24.Bin_ALeft",
    "CC24.Bin_ARight",
    "CC25.Bin_ARight",
    "CC26.Bin_ALeft",
    "CC26.Bin_ARight",
    "CC27.Bin_ARight",
    "CC28.Bin_ALeft",
    "CC28.Bin_ARight",
    "CC29.Bin_ARight",
    "CC30.Bin_ALeft",
    "CC30.Bin_ARight",
    "CC31.Bin_ARight",
    "CC32.Bin_ALeft",
    "CC32.Bin_ARight",
    "CC36.Bin_ALeft",
    "CC36.Bin_ARight",
    "CC37.Bin_ARight",
    "CC38.Bin_ALeft",
    "CC38.Bin_ARight",
    "CC39.Bin_ARight",
    "CC40.Bin_ALeft",
    "CC40.Bin_ARight",
    "CC41.Bin_ARight",
    "CC42.Bin_ALeft",
    "CC42.Bin_ARight",
    "CC43.Bin_ARight",
    "CC44.Bin_ALeft",
    "CC44.Bin_ARight",
    "CC45.Bin_ARight",
    "CC46.Bin_ALeft",
    "CC46.Bin_ARight",
    "CC47.Bin_ARight",
    "CC48.Bin_ALeft",
    "CC48.Bin_ARight",
    "CC49.Bin_ARight",
    "CC50.Bin_ALeft",
    "CC50.Bin_ARight",
    "CC51.Bin_ARight",
    "CC52.Bin_ALeft",
    "CC52.Bin_ARight",
    "CC53.Bin_ARight",
    "CC54.Bin_ALeft",
    "CC54.Bin_ARight",
    "CC55.Bin_ARight",
    "CC56.Bin_ALeft",
    "CC56.Bin_ARight",
    "CC57.Bin_ARight",
    "CC58.Bin_ALeft",
    "CC58.Bin_ARight",
    "CC59.Bin_ARight",
    "CC60.Bin_ALeft",
    "CC60.Bin_ARight",
    "CC61.Bin_ARight",
    "CC62.Bin_ALeft",
    "CC62.Bin_ARight",
    "CC63.Bin_ARight",
    "CC64.Bin_ALeft",
    "CC64.Bin_ARight",
    "CC65.Bin_ARight",
    "CC66.Bin_ALeft",
    "CC66.Bin_ARight",
    "CC67.Bin_ARight",
    "CC68.Bin_ALeft",
    "CC68.Bin_ARight",
    "CC69.Bin_ARight",
    "CC70.Bin_ALeft",
    "CC70.Bin_ARight",
    "CC71.Bin_ARight",
    "CC72.Bin_ALeft",
    "CC72.Bin_ARight",
    "CC73.Bin_ARight",
    "CC74.Bin_ALeft",
    "CC74.Bin_ARight",
    "CC75.Bin_ARight"
]

prefix_list_all = prefix_list_B + prefix_list_A

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

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [filename.xlsx]")
        sys.exit(1)

    file_path = sys.argv[1]
    df = pd.read_excel(file_path)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['_VAL'] = df['_VAL'].fillna(0).astype(int)

    all_alarms = []
    prefix_to_sub_alarms = {}
    for prefix in prefix_list_all:
        sub_alarms = [prefix + sfx for sfx in suffixes]
        prefix_to_sub_alarms[prefix] = sub_alarms
        all_alarms.extend(sub_alarms)
    
    df = df[df['point_id'].isin(all_alarms)]
    
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

    # alarm_hour_data[prefix][hour_index] = [downtime_seconds, trigger_count]
    alarm_hour_data = {
        prefix: {i: [0.0, 0] for i in range(NUM_HOURS)}
        for prefix in prefix_list_all
    }

    def accumulate_intervals(prefix, intervals, add_triggers=False):
        """
        prefix: e.g. 'CC6.Bin_BRight'
        intervals: list of (start_ts, end_ts) for that alarm
        add_triggers: if True, we add 'trigger_count' from these intervals
        """
        day_start = hourly_intervals[0][0]
        day_end   = hourly_intervals[-1][1]  # end of the last hour

        for (start_ts, end_ts) in intervals:
            # skip if no overlap
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

    for prefix in prefix_list_all:
        sub_alarms = prefix_to_sub_alarms[prefix]
        # sub_alarms = [prefix+"_Full", prefix+"_NotPresent", prefix+"_PresentNotResumed"]

        intervals_map = {}
        for point_id in sub_alarms:
            df_sub = df[df['point_id'] == point_id]
            if df_sub.empty:
                intervals_map[point_id] = []
            else:
                intervals_map[point_id] = build_intervals_per_alarm(df_sub)

        for point_id in sub_alarms:
            add_trigs = (point_id.endswith("_Full"))
            accumulate_intervals(prefix, intervals_map[point_id], add_trigs)

    rows = []
    for prefix in prefix_list_all:
        row_dict = {"point_id": prefix}
        for i, (bucket_start, bucket_end) in enumerate(hourly_intervals):
            sec = alarm_hour_data[prefix][i][0]  # total downtime seconds
            trig = alarm_hour_data[prefix][i][1] # trigger count
            row_dict[count_cols[i]] = trig
            row_dict[downtime_cols[i]] = sec
        rows.append(row_dict)
    
    results = pd.DataFrame(rows)

    def get_sort_index(pfx):
        return prefix_list_all.index(pfx)
    results['sort_order'] = results['point_id'].apply(get_sort_index)
    results = results.sort_values('sort_order').drop(columns=['sort_order'])

    def subset_df_by_bin(results_df, bin_label):
        # e.g. bin_label = 'Bin_B' or 'Bin_A'
        mask = results_df['point_id'].str.contains(bin_label)
        return results_df[mask].copy()

    df_binB = subset_df_by_bin(results, 'Bin_B')
    df_binA = subset_df_by_bin(results, 'Bin_A')

    def export_triggers_and_downtime(df_in, bin_label):
        # trigger counts only
        results_counts = df_in[['point_id'] + count_cols].copy()
        rename_map_counts = {col: col.replace("_count", "") for col in count_cols}
        results_counts = results_counts.rename(columns=rename_map_counts)
        results_counts.to_csv(f"hourly-trigger-{bin_label}.csv", index=False)

        # Downtime only
        results_downtime = df_in[['point_id'] + downtime_cols].copy()
        rename_map_downtime = {col: col.replace("_downtime", "") for col in downtime_cols}
        results_downtime = results_downtime.rename(columns=rename_map_downtime)
        results_downtime.to_csv(f"hourly-downtime-{bin_label}.csv", index=False)

    # export BinB
    export_triggers_and_downtime(df_binB, "BinB")
    print("BinB trigger  => hourly-trigger-BinB.csv")
    print("BinB downtime => hourly-downtime-BinB.csv")

    # export BinA
    export_triggers_and_downtime(df_binA, "BinA")
    print("BinA trigger  => hourly-trigger-BinA.csv")
    print("BinA downtime => hourly-downtime-BinA.csv")


if __name__ == "__main__":
    main()
