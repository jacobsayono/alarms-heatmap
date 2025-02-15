import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import table
import matplotlib.colors as mcolors
import sys

if len(sys.argv) != 2:
    print("Usage: python3 script.py [filename.xlsx]")
    sys.exit(1)

file_path = sys.argv[1]

df = pd.read_excel(file_path)

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['log_action'] = df['log_action'].astype(str).fillna('0')

df = df.sort_values(by='timestamp')

# init dict for 2 features
total_time_differences = {}
trigger_counts = {}

# iter thru rows of data table
for _, row in df.iterrows():
    alarm_id = row['alarm_id']
    log_action = row['log_action']
    timestamp = row['timestamp']

    # init trigger time if it's the first time seeing this alarm_id
    if alarm_id not in trigger_counts:
        trigger_counts[alarm_id] = 0
        total_time_differences[alarm_id] = pd.Timedelta(0)

    # when a trigger is encountered (log_action = 1)
    if log_action == 'G':
        trigger_counts[alarm_id] += 1
        trigger_time = timestamp

    # when a resolution is encountered (log_action = 0)
    elif log_action == 'R' and alarm_id in trigger_counts:
        # only process if there was a trigger before this resolution
        if trigger_counts[alarm_id] > 0:
            time_diff = timestamp - trigger_time  # calc time difference
            total_time_differences[alarm_id] += time_diff  # add to total time

# map row/col of our MaRS system
row_col_mapping = {
    # transfer conveyor 1
    "TC1.TC1_FaultNoES": (0,0),
    "TC1.TC2_FaultNoES": (0,1),
    "TC1.TC3_FaultNoES": (0,2),
    "TC1.TC4_FaultNoES": (0,3),
    "TC1.TC5_FaultNoES": (0,4),
    "TC1.TC6_FaultNoES": (0,5),
    "TC1.TC7_FaultNoES": (0,6),

    # transfer conveyor 2
    "TC2.TC1_FaultNoES": (1,0),
    "TC2.TC2_FaultNoES": (1,1),
    "TC2.TC3_FaultNoES": (1,2),
    "TC2.TC4_FaultNoES": (1,3),
    "TC2.TC5_FaultNoES": (1,4),
    "TC2.TC6_FaultNoES": (1,5),
    "TC2.TC7_FaultNoES": (1,6),

    # transfer conveyor 3
    "TC3.TC1_FaultNoES": (2,0),
    "TC3.TC2_FaultNoES": (2,1),
    "TC3.TC3_FaultNoES": (2,2),
    "TC3.TC4_FaultNoES": (2,3),
    "TC3.TC5_FaultNoES": (2,4),
    "TC3.TC6_FaultNoES": (2,5),
    "TC3.TC7_FaultNoES": (2,6),

    # transfer conveyor 4
    "TC4.TC1_FaultNoES": (3,0),
    "TC4.TC2_FaultNoES": (3,1),
    "TC4.TC3_FaultNoES": (3,2),
    "TC4.TC4_FaultNoES": (3,3),
    "TC4.TC5_FaultNoES": (3,4),
    "TC4.TC6_FaultNoES": (3,5),
    "TC4.TC7_FaultNoES": (3,6),

    # transfer conveyor 5
    "TC5.TC1_FaultNoES": (4,0),
    "TC5.TC2_FaultNoES": (4,1),
    "TC5.TC3_FaultNoES": (4,2),
    "TC5.TC4_FaultNoES": (4,3),
    "TC5.TC5_FaultNoES": (4,4),
    "TC5.TC6_FaultNoES": (4,5),
    "TC5.TC7_FaultNoES": (4,6),

    # transfer conveyor 6
    "TC6.TC1_FaultNoES": (5,0),
    "TC6.TC2_FaultNoES": (5,1),
    "TC6.TC3_FaultNoES": (5,2),
    "TC6.TC4_FaultNoES": (5,3),
    "TC6.TC5_FaultNoES": (5,4),
    "TC6.TC6_FaultNoES": (5,5),
    "TC6.TC7_FaultNoES": (5,6),

    # transfer conveyor 7
    "TC7.TC1_FaultNoES": (6,0),
    "TC7.TC2_FaultNoES": (6,1),
    "TC7.TC3_FaultNoES": (6,2),
    "TC7.TC4_FaultNoES": (6,3),
    "TC7.TC5_FaultNoES": (6,4),
    "TC7.TC6_FaultNoES": (6,5),
    "TC7.TC7_FaultNoES": (6,6),

    # transfer conveyor 8
    "TC8.TC1_FaultNoES": (7,0),
    "TC8.TC2_FaultNoES": (7,1),
    "TC8.TC3_FaultNoES": (7,2),
    "TC8.TC4_FaultNoES": (7,3),
    "TC8.TC5_FaultNoES": (7,4),
    "TC8.TC6_FaultNoES": (7,5),
    "TC8.TC7_FaultNoES": (7,6),
}

# create dataframe with appropriate size (indiana 8 strands, 27 singulator columns) for heatmap generation
rows = 8
cols = 7
table_df = pd.DataFrame("", index=range(rows), columns=range(cols), dtype=object)

trigger_values = {}
for alarm_id, trigger in trigger_counts.items():
    if alarm_id in row_col_mapping:
        row, col = row_col_mapping[alarm_id]
        # table_df.loc[row, col] = trigger
        # table_df.loc[row, col] = ""
        trigger_values[(row, col)] = trigger

# row and col titles
table_df.index = ['Strand 1', 'Strand 2', 'Strand 3', 'Strand 4', 'Strand 5', 'Strand 6', 'Strand 7', 'Strand 8']
table_df.columns = ['TC1', 'TC2', 'TC3', 'TC4', 'TC5', 'TC6', 'TC7']

# absolute count range for color mapping
min_count = 0  # min trigger count
max_count = max(trigger_values.values())  # max trigger count
# max_count = 20  # or custom max val
norm = mcolors.Normalize(vmin=min_count, vmax=max_count)
cmap = plt.colormaps.get_cmap("gnuplot2_r")  # different coloring on cmap() documentation

# # create cell colours based on trigger counts
# cell_colours = np.full((rows, cols), '#FFFFFF')  # init color grid
# for alarm_id, trigger in trigger_counts.items():
#     if alarm_id in row_col_mapping:
#         row, col = row_col_mapping[alarm_id]
#         color = cmap(norm(trigger))  # get color for the current trigger count
#         cell_colours[row, col] = mcolors.to_hex(color)  # convert to hex

# for alarm_id, (row, col) in row_col_mapping.items():
#     if alarm_id in trigger_counts:
#         count = trigger_counts[alarm_id]
#         color = cmap(norm(count))
#         cell_colours[row, col] = mcolors.to_hex(color)

cell_colours = np.full((rows, cols), '#FFFFFF')  # init color grid
for (row, col), count in trigger_values.items():
    color = cmap(norm(count))  # get color for the current trigger count
    cell_colours[row, col] = mcolors.to_hex(color)  # convert to hex



# cell_colours = np.full((rows, cols), '#FFFFFF')  # init color grid
# for alarm_id, trigger_count in trigger_counts.items():
#     if alarm_id in row_col_mapping:
#         row, col = row_col_mapping[alarm_id]
#         color = cmap(norm(trigger_count))        # get color for the trigger count
#         cell_colours[row, col] = mcolors.to_hex(color)  # convert to hex


# figure size
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# fig.suptitle("Alarm Events Heatmap", fontsize=16)  # title for the entire figure
# ax.set_title("Total Trigger Counts by Photo-Eye Jams", fontsize=14)  # title for the subplot


# heatmap's col widths
# tbl = table(ax, table_df, loc='center', colWidths=[0.1] * cols, cellColours=cell_colours)
tbl = table(ax, table_df, loc='center', colWidths=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05], cellColours=cell_colours)


tbl.auto_set_font_size(False)
tbl.set_fontsize(7)
tbl.scale(0.7, 0.7)

# add colorbar on the right to indicate the feature (time range) from lo to hi
cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.02])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # empty array for scalarmappable
cbar = fig.colorbar(sm, cax=cbar_ax, label='Trigger Counts', orientation='horizontal')

# set ticks on the colorbar
# cbar.set_ticks([min_count, (max_count/3), (2*max_count/3), max_count])  # set ticks for min, mid, and max trigger counts
# cbar.set_ticklabels([int(min_count), int(max_count/3), int(2*max_count/3), int(max_count)])  # format ticks as integers
cbar.set_ticks([min_count, (max_count/10), (2*max_count/10), (3*max_count/10), (4*max_count/10), (5*max_count/10), (6*max_count/10), (7*max_count/10), (8*max_count/10), (9*max_count/10), max_count])  # set ticks for min, mid, and max trigger counts
cbar.set_ticklabels([min_count, float(max_count/10), 2*max_count/10, 3*max_count/10, 4*max_count/10, 5*max_count/10, 6*max_count/10, 7*max_count/10, 8*max_count/10, 9*max_count/10, max_count])  # format ticks as integers


# show figure
plt.show()
