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
df['point_val'] = df['point_val'].fillna(0).astype(int)

df = df.sort_values(by='timestamp')

# init dict for 2 features
total_time_differences = {}
trigger_counts = {}

# iter thru rows of data table
for _, row in df.iterrows():
    alarm_id = row['alarm_id']
    point_val = row['point_val']
    timestamp = row['timestamp']

    # init trigger time if it's the first time seeing this alarm_id
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

# map row/col of our MaRS system
row_col_mapping = {
    # singulator1
    # "SINGULATOR1.Singulator_U1U2_Jam": (0,0),
    "SINGULATOR1.D0_PHTEYE_JAM": (0,1),
    "SINGULATOR1.D1_PHTEYE_JAM": (0,2),
    "SINGULATOR1.D2_PHTEYE_JAM": (0,3),
    "SINGULATOR1.D3_PHTEYE_JAM": (0,4),
    "SINGULATOR1.D4_PHTEYE_JAM": (0,5),
    "SINGULATOR1.D5_PHTEYE_JAM": (0,6),
    "SINGULATOR1.F1_PHTEYE_JAM": (0,7),
    "SINGULATOR1.F2_PHTEYE_JAM": (0,8),
    "SINGULATOR1.F3_PHTEYE_JAM": (0,9),
    "SINGULATOR1.VIS_PHTEYE_JAM_FLT": (0,10),
    "SINGULATOR1.MG1_PHTEYE_JAM": (0,11),
    "SINGULATOR1.MG2_PHTEYE_JAM": (0,12),
    "SINGULATOR1.MG3_PHTEYE_JAM": (0,13),
    "SINGULATOR1.MG4_PHTEYE_JAM": (0,14),
    "SINGULATOR1.AL0_PHTEYE_JAM": (0,15),
    "SINGULATOR1.PG1_PHTEYE_JAM": (0,16),
    "SINGULATOR1.G1_PHTEYE_JAM": (0,17),
    "SINGULATOR1.G2_PHTEYE_JAM": (0,18),
    "SINGULATOR1.G3_PHTEYE_JAM": (0,19),
    "SINGULATOR1.G4_PHTEYE_JAM": (0,20),
    "SINGULATOR1.G5_PHTEYE_JAM": (0,21),
    "SINGULATOR1.G6_PHTEYE_JAM": (0,22),
    "SINGULATOR1.G7_PHTEYE_JAM": (0,23),
    "SINGULATOR1.G8_PHTEYE_JAM": (0,24),
    "SINGULATOR1.G9_PHTEYE_JAM": (0,25),
    "SINGULATOR1.G10_PHTEYE_JAM": (0,26),

    #singulator2
    "SINGULATOR2.D0_PHTEYE_JAM": (1,1),
    "SINGULATOR2.D1_PHTEYE_JAM": (1,2),
    "SINGULATOR2.D2_PHTEYE_JAM": (1,3),
    "SINGULATOR2.D3_PHTEYE_JAM": (1,4),
    "SINGULATOR2.D4_PHTEYE_JAM": (1,5),
    "SINGULATOR2.D5_PHTEYE_JAM": (1,6),
    "SINGULATOR2.F1_PHTEYE_JAM": (1,7),
    "SINGULATOR2.F2_PHTEYE_JAM": (1,8),
    "SINGULATOR2.F3_PHTEYE_JAM": (1,9),
    "SINGULATOR2.VIS_PHTEYE_JAM_FLT": (1,10),
    "SINGULATOR2.MG1_PHTEYE_JAM": (1,11),
    "SINGULATOR2.MG2_PHTEYE_JAM": (1,12),
    "SINGULATOR2.MG3_PHTEYE_JAM": (1,13),
    "SINGULATOR2.MG4_PHTEYE_JAM": (1,14),
    "SINGULATOR2.AL0_PHTEYE_JAM": (1,15),
    "SINGULATOR2.PG1_PHTEYE_JAM": (1,16),
    "SINGULATOR2.G1_PHTEYE_JAM": (1,17),
    "SINGULATOR2.G2_PHTEYE_JAM": (1,18),
    "SINGULATOR2.G3_PHTEYE_JAM": (1,19),
    "SINGULATOR2.G4_PHTEYE_JAM": (1,20),
    "SINGULATOR2.G5_PHTEYE_JAM": (1,21),
    "SINGULATOR2.G6_PHTEYE_JAM": (1,22),
    "SINGULATOR2.G7_PHTEYE_JAM": (1,23),
    "SINGULATOR2.G8_PHTEYE_JAM": (1,24),
    "SINGULATOR2.G9_PHTEYE_JAM": (1,25),
    "SINGULATOR2.G10_PHTEYE_JAM": (1,26),
    
    #singulator3
    "SINGULATOR3.D0_PHTEYE_JAM": (2,1),
    "SINGULATOR3.D1_PHTEYE_JAM": (2,2),
    "SINGULATOR3.D2_PHTEYE_JAM": (2,3),
    "SINGULATOR3.D3_PHTEYE_JAM": (2,4),
    "SINGULATOR3.D4_PHTEYE_JAM": (2,5),
    "SINGULATOR3.D5_PHTEYE_JAM": (2,6),
    "SINGULATOR3.F1_PHTEYE_JAM": (2,7),
    "SINGULATOR3.F2_PHTEYE_JAM": (2,8),
    "SINGULATOR3.F3_PHTEYE_JAM": (2,9),
    "SINGULATOR3.VIS_PHTEYE_JAM_FLT": (2,10),
    "SINGULATOR3.MG1_PHTEYE_JAM": (2,11),
    "SINGULATOR3.MG2_PHTEYE_JAM": (2,12),
    "SINGULATOR3.MG3_PHTEYE_JAM": (2,13),
    "SINGULATOR3.MG4_PHTEYE_JAM": (2,14),
    "SINGULATOR3.AL0_PHTEYE_JAM": (2,15),
    "SINGULATOR3.PG1_PHTEYE_JAM": (2,16),
    "SINGULATOR3.G1_PHTEYE_JAM": (2,17),
    "SINGULATOR3.G2_PHTEYE_JAM": (2,18),
    "SINGULATOR3.G3_PHTEYE_JAM": (2,19),
    "SINGULATOR3.G4_PHTEYE_JAM": (2,20),
    "SINGULATOR3.G5_PHTEYE_JAM": (2,21),
    "SINGULATOR3.G6_PHTEYE_JAM": (2,22),
    "SINGULATOR3.G7_PHTEYE_JAM": (2,23),
    "SINGULATOR3.G8_PHTEYE_JAM": (2,24),
    "SINGULATOR3.G9_PHTEYE_JAM": (2,25),
    "SINGULATOR3.G10_PHTEYE_JAM": (2,26),

    #singulator4
    "SINGULATOR4.D0_PHTEYE_JAM": (3,1),
    "SINGULATOR4.D1_PHTEYE_JAM": (3,2),
    "SINGULATOR4.D2_PHTEYE_JAM": (3,3),
    "SINGULATOR4.D3_PHTEYE_JAM": (3,4),
    "SINGULATOR4.D4_PHTEYE_JAM": (3,5),
    "SINGULATOR4.D5_PHTEYE_JAM": (3,6),
    "SINGULATOR4.F1_PHTEYE_JAM": (3,7),
    "SINGULATOR4.F2_PHTEYE_JAM": (3,8),
    "SINGULATOR4.F3_PHTEYE_JAM": (3,9),
    "SINGULATOR4.VIS_PHTEYE_JAM_FLT": (3,10),
    "SINGULATOR4.MG1_PHTEYE_JAM": (3,11),
    "SINGULATOR4.MG2_PHTEYE_JAM": (3,12),
    "SINGULATOR4.MG3_PHTEYE_JAM": (3,13),
    "SINGULATOR4.MG4_PHTEYE_JAM": (3,14),
    "SINGULATOR4.AL0_PHTEYE_JAM": (3,15),
    "SINGULATOR4.PG1_PHTEYE_JAM": (3,16),
    "SINGULATOR4.G1_PHTEYE_JAM": (3,17),
    "SINGULATOR4.G2_PHTEYE_JAM": (3,18),
    "SINGULATOR4.G3_PHTEYE_JAM": (3,19),
    "SINGULATOR4.G4_PHTEYE_JAM": (3,20),
    "SINGULATOR4.G5_PHTEYE_JAM": (3,21),
    "SINGULATOR4.G6_PHTEYE_JAM": (3,22),
    "SINGULATOR4.G7_PHTEYE_JAM": (3,23),
    "SINGULATOR4.G8_PHTEYE_JAM": (3,24),
    "SINGULATOR4.G9_PHTEYE_JAM": (3,25),
    "SINGULATOR4.G10_PHTEYE_JAM": (3,26),
    
    #singulator5
    "SINGULATOR5.D0_PHTEYE_JAM": (4,1),
    "SINGULATOR5.D1_PHTEYE_JAM": (4,2),
    "SINGULATOR5.D2_PHTEYE_JAM": (4,3),
    "SINGULATOR5.D3_PHTEYE_JAM": (4,4),
    "SINGULATOR5.D4_PHTEYE_JAM": (4,5),
    "SINGULATOR5.D5_PHTEYE_JAM": (4,6),
    "SINGULATOR5.F1_PHTEYE_JAM": (4,7),
    "SINGULATOR5.F2_PHTEYE_JAM": (4,8),
    "SINGULATOR5.F3_PHTEYE_JAM": (4,9),
    "SINGULATOR5.VIS_PHTEYE_JAM_FLT": (4,10),
    "SINGULATOR5.MG1_PHTEYE_JAM": (4,11),
    "SINGULATOR5.MG2_PHTEYE_JAM": (4,12),
    "SINGULATOR5.MG3_PHTEYE_JAM": (4,13),
    "SINGULATOR5.MG4_PHTEYE_JAM": (4,14),
    "SINGULATOR5.AL0_PHTEYE_JAM": (4,15),
    "SINGULATOR5.PG1_PHTEYE_JAM": (4,16),
    "SINGULATOR5.G1_PHTEYE_JAM": (4,17),
    "SINGULATOR5.G2_PHTEYE_JAM": (4,18),
    "SINGULATOR5.G3_PHTEYE_JAM": (4,19),
    "SINGULATOR5.G4_PHTEYE_JAM": (4,20),
    "SINGULATOR5.G5_PHTEYE_JAM": (4,21),
    "SINGULATOR5.G6_PHTEYE_JAM": (4,22),
    "SINGULATOR5.G7_PHTEYE_JAM": (4,23),
    "SINGULATOR5.G8_PHTEYE_JAM": (4,24),
    "SINGULATOR5.G9_PHTEYE_JAM": (4,25),
    "SINGULATOR5.G10_PHTEYE_JAM": (4,26),

    #singulator6
    "SINGULATOR6.D0_PHTEYE_JAM": (5,1),
    "SINGULATOR6.D1_PHTEYE_JAM": (5,2),
    "SINGULATOR6.D2_PHTEYE_JAM": (5,3),
    "SINGULATOR6.D3_PHTEYE_JAM": (5,4),
    "SINGULATOR6.D4_PHTEYE_JAM": (5,5),
    "SINGULATOR6.D5_PHTEYE_JAM": (5,6),
    "SINGULATOR6.F1_PHTEYE_JAM": (5,7),
    "SINGULATOR6.F2_PHTEYE_JAM": (5,8),
    "SINGULATOR6.F3_PHTEYE_JAM": (5,9),
    "SINGULATOR6.VIS_PHTEYE_JAM_FLT": (5,10),
    "SINGULATOR6.MG1_PHTEYE_JAM": (5,11),
    "SINGULATOR6.MG2_PHTEYE_JAM": (5,12),
    "SINGULATOR6.MG3_PHTEYE_JAM": (5,13),
    "SINGULATOR6.MG4_PHTEYE_JAM": (5,14),
    "SINGULATOR6.AL0_PHTEYE_JAM": (5,15),
    "SINGULATOR6.PG1_PHTEYE_JAM": (5,16),
    "SINGULATOR6.G1_PHTEYE_JAM": (5,17),
    "SINGULATOR6.G2_PHTEYE_JAM": (5,18),
    "SINGULATOR6.G3_PHTEYE_JAM": (5,19),
    "SINGULATOR6.G4_PHTEYE_JAM": (5,20),
    "SINGULATOR6.G5_PHTEYE_JAM": (5,21),
    "SINGULATOR6.G6_PHTEYE_JAM": (5,22),
    "SINGULATOR6.G7_PHTEYE_JAM": (5,23),
    "SINGULATOR6.G8_PHTEYE_JAM": (5,24),
    "SINGULATOR6.G9_PHTEYE_JAM": (5,25),
    "SINGULATOR6.G10_PHTEYE_JAM": (5,26),

    #singulator7
    "SINGULATOR7.D0_PHTEYE_JAM": (6,1),
    "SINGULATOR7.D1_PHTEYE_JAM": (6,2),
    "SINGULATOR7.D2_PHTEYE_JAM": (6,3),
    "SINGULATOR7.D3_PHTEYE_JAM": (6,4),
    "SINGULATOR7.D4_PHTEYE_JAM": (6,5),
    "SINGULATOR7.D5_PHTEYE_JAM": (6,6),
    "SINGULATOR7.F1_PHTEYE_JAM": (6,7),
    "SINGULATOR7.F2_PHTEYE_JAM": (6,8),
    "SINGULATOR7.F3_PHTEYE_JAM": (6,9),
    "SINGULATOR7.VIS_PHTEYE_JAM_FLT": (6,10),
    "SINGULATOR7.MG1_PHTEYE_JAM": (6,11),
    "SINGULATOR7.MG2_PHTEYE_JAM": (6,12),
    "SINGULATOR7.MG3_PHTEYE_JAM": (6,13),
    "SINGULATOR7.MG4_PHTEYE_JAM": (6,14),
    "SINGULATOR7.AL0_PHTEYE_JAM": (6,15),
    "SINGULATOR7.PG1_PHTEYE_JAM": (6,16),
    "SINGULATOR7.G1_PHTEYE_JAM": (6,17),
    "SINGULATOR7.G2_PHTEYE_JAM": (6,18),
    "SINGULATOR7.G3_PHTEYE_JAM": (6,19),
    "SINGULATOR7.G4_PHTEYE_JAM": (6,20),
    "SINGULATOR7.G5_PHTEYE_JAM": (6,21),
    "SINGULATOR7.G6_PHTEYE_JAM": (6,22),
    "SINGULATOR7.G7_PHTEYE_JAM": (6,23),
    "SINGULATOR7.G8_PHTEYE_JAM": (6,24),
    "SINGULATOR7.G9_PHTEYE_JAM": (6,25),
    "SINGULATOR7.G10_PHTEYE_JAM": (6,26),

    #singulator8
    "SINGULATOR8.D0_PHTEYE_JAM": (7,1),
    "SINGULATOR8.D1_PHTEYE_JAM": (7,2),
    "SINGULATOR8.D2_PHTEYE_JAM": (7,3),
    "SINGULATOR8.D3_PHTEYE_JAM": (7,4),
    "SINGULATOR8.D4_PHTEYE_JAM": (7,5),
    "SINGULATOR8.D5_PHTEYE_JAM": (7,6),
    "SINGULATOR8.F1_PHTEYE_JAM": (7,7),
    "SINGULATOR8.F2_PHTEYE_JAM": (7,8),
    "SINGULATOR8.F3_PHTEYE_JAM": (7,9),
    "SINGULATOR8.VIS_PHTEYE_JAM_FLT": (7,10),
    "SINGULATOR8.MG1_PHTEYE_JAM": (7,11),
    "SINGULATOR8.MG2_PHTEYE_JAM": (7,12),
    "SINGULATOR8.MG3_PHTEYE_JAM": (7,13),
    "SINGULATOR8.MG4_PHTEYE_JAM": (7,14),
    "SINGULATOR8.AL0_PHTEYE_JAM": (7,15),
    "SINGULATOR8.PG1_PHTEYE_JAM": (7,16),
    "SINGULATOR8.G1_PHTEYE_JAM": (7,17),
    "SINGULATOR8.G2_PHTEYE_JAM": (7,18),
    "SINGULATOR8.G3_PHTEYE_JAM": (7,19),
    "SINGULATOR8.G4_PHTEYE_JAM": (7,20),
    "SINGULATOR8.G5_PHTEYE_JAM": (7,21),
    "SINGULATOR8.G6_PHTEYE_JAM": (7,22),
    "SINGULATOR8.G7_PHTEYE_JAM": (7,23),
    "SINGULATOR8.G8_PHTEYE_JAM": (7,24),
    "SINGULATOR8.G9_PHTEYE_JAM": (7,25),
    "SINGULATOR8.G10_PHTEYE_JAM": (7,26),
}

# create dataframe with appropriate size (chicago 8 strand rows, 27 singulator columns) for heatmap generation
rows = 8
cols = 27
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
table_df.columns = ['U1U2', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'F1', 'F2', 'F3', 'VIS', 'MG1', 'MG2', 'MG3', 'MG4', 'AL0', 'PG1', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']

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
tbl = table(ax, table_df, loc='center', colWidths=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.1, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05], cellColours=cell_colours)


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
