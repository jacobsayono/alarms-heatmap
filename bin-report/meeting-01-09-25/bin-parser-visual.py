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

total_time_differences = {}
trigger_counts = {}

for _, row in df.iterrows():
    alarm_id = row['alarm_id']
    point_val = row['point_val']
    timestamp = row['timestamp']

    if alarm_id not in trigger_counts:
        trigger_counts[alarm_id] = 0
        total_time_differences[alarm_id] = pd.Timedelta(0)

    if point_val == 1:
        trigger_counts[alarm_id] += 1
        trigger_time = timestamp

    elif point_val == 0 and alarm_id in trigger_counts:
        if trigger_counts[alarm_id] > 0:
            time_diff = timestamp - trigger_time
            total_time_differences[alarm_id] += time_diff

row_col_mapping = {
        
    "CC1.Bin_BLeft_Full": (0,0),
    "CC1.Bin_BRight_Full": (1,0),

    "CC2.Bin_BLeft_Full": (0,1),
    "CC2.Bin_BRight_Full": (1,1),

    "CC3.Bin_BLeft_Full": (0,2),
    "CC3.Bin_BRight_Full": (1,2),

    "CC4.Bin_BLeft_Full": (0,3),
    "CC4.Bin_BRight_Full": (1,3),

    "CC5.Bin_BLeft_Full": (0,4),
    "CC5.Bin_BRight_Full": (1,4),

    "CC6.Bin_BLeft_Full": (0,5),
    "CC6.Bin_BRight_Full": (1,5),

    "CC7.Bin_BLeft_Full": (0,6),
    "CC7.Bin_BRight_Full": (1,6),

    "CC8.Bin_BLeft_Full": (0,7),
    "CC8.Bin_BRight_Full": (1,7),

    "CC9.Bin_BLeft_Full": (0,8),
    "CC9.Bin_BRight_Full": (1,8),

    "CC10.Bin_BLeft_Full": (0,9),
    "CC10.Bin_BRight_Full": (1,9),

    "CC11.Bin_BLeft_Full": (0,10),
    "CC11.Bin_BRight_Full": (1,10),

    "CC12.Bin_BLeft_Full": (0,11),
    "CC12.Bin_BRight_Full": (1,11),

    "CC13.Bin_BLeft_Full": (0,12),
    "CC13.Bin_BRight_Full": (1,12),

    "CC14.Bin_BLeft_Full": (0,13),
    "CC14.Bin_BRight_Full": (1,13),

    "CC15.Bin_BLeft_Full": (0,14),
    "CC15.Bin_BRight_Full": (1,14),

    "CC16.Bin_BLeft_Full": (0,15),
    "CC16.Bin_BRight_Full": (1,15),

    "CC17.Bin_BLeft_Full": (0,16),
    "CC17.Bin_BRight_Full": (1,16),

    "CC18.Bin_BLeft_Full": (0,17),
    "CC18.Bin_BRight_Full": (1,17),

    "CC19.Bin_BLeft_Full": (0,18),
    "CC19.Bin_BRight_Full": (1,18),

    "CC20.Bin_BLeft_Full": (0,19),
    "CC20.Bin_BRight_Full": (1,19),

    "CC21.Bin_BLeft_Full": (0,20),
    "CC21.Bin_BRight_Full": (1,20),

    "CC22.Bin_BLeft_Full": (0,21),
    "CC22.Bin_BRight_Full": (1,21),

    "CC23.Bin_BLeft_Full": (0,22),
    "CC23.Bin_BRight_Full": (1,22),

    "CC24.Bin_BLeft_Full": (0,23),
    "CC24.Bin_BRight_Full": (1,23),

    "CC25.Bin_BLeft_Full": (0,24),
    "CC25.Bin_BRight_Full": (1,24),

    "CC26.Bin_BLeft_Full": (0,25),
    "CC26.Bin_BRight_Full": (1,25),

    "CC27.Bin_BLeft_Full": (0,26),
    "CC27.Bin_BRight_Full": (1,26),

    "CC28.Bin_BLeft_Full": (0,27),
    "CC28.Bin_BRight_Full": (1,27),

    "CC29.Bin_BLeft_Full": (0,28),
    "CC29.Bin_BRight_Full": (1,28),

    "CC30.Bin_BLeft_Full": (0,29),
    "CC30.Bin_BRight_Full": (1,29),

    "CC31.Bin_BLeft_Full": (0,30),
    "CC31.Bin_BRight_Full": (1,30),

    "CC32.Bin_BLeft_Full": (0,31),
    "CC32.Bin_BRight_Full": (1,31),

    "CC33.Bin_BLeft_Full": (0,32),
    "CC33.Bin_BRight_Full": (1,32),

    "CC34.Bin_BLeft_Full": (0,33),
    "CC34.Bin_BRight_Full": (1,33),

    "CC35.Bin_BLeft_Full": (0,34),
    "CC35.Bin_BRight_Full": (1,34),

    "CC36.Bin_BLeft_Full": (0,35),
    "CC36.Bin_BRight_Full": (1,35),

    "CC37.Bin_BLeft_Full": (0,36),
    "CC37.Bin_BRight_Full": (1,36),

    "CC38.Bin_BLeft_Full": (0,37),
    "CC38.Bin_BRight_Full": (1,37),

    "CC39.Bin_BLeft_Full": (0,38),
    "CC39.Bin_BRight_Full": (1,38),

    "CC40.Bin_BLeft_Full": (0,39),
    "CC40.Bin_BRight_Full": (1,39),

    "CC41.Bin_BLeft_Full": (0,40),
    "CC41.Bin_BRight_Full": (1,40),

    "CC42.Bin_BLeft_Full": (0,41),
    "CC42.Bin_BRight_Full": (1,41),

    "CC43.Bin_BLeft_Full": (0,42),
    "CC43.Bin_BRight_Full": (1,42),

    "CC44.Bin_BLeft_Full": (0,43),
    "CC44.Bin_BRight_Full": (1,43),

    "CC45.Bin_BLeft_Full": (0,44),
    "CC45.Bin_BRight_Full": (1,44),

    "CC46.Bin_BLeft_Full": (0,45),
    "CC46.Bin_BRight_Full": (1,45),

    "CC47.Bin_BLeft_Full": (0,46),
    "CC47.Bin_BRight_Full": (1,46),

    "CC48.Bin_BLeft_Full": (0,47),
    "CC48.Bin_BRight_Full": (1,47),

    "CC49.Bin_BLeft_Full": (0,48),
    "CC49.Bin_BRight_Full": (1,48),

    "CC50.Bin_BLeft_Full": (0,49),
    "CC50.Bin_BRight_Full": (1,49),

    "CC51.Bin_BLeft_Full": (0,50),
    "CC51.Bin_BRight_Full": (1,50),

    "CC52.Bin_BLeft_Full": (0,51),
    "CC52.Bin_BRight_Full": (1,51),

    "CC53.Bin_BLeft_Full": (0,52),
    "CC53.Bin_BRight_Full": (1,52),

    "CC54.Bin_BLeft_Full": (0,53),
    "CC54.Bin_BRight_Full": (1,53),

    "CC55.Bin_BLeft_Full": (0,54),
    "CC55.Bin_BRight_Full": (1,54),

    "CC56.Bin_BLeft_Full": (0,55),
    "CC56.Bin_BRight_Full": (1,55),

    "CC57.Bin_BLeft_Full": (0,56),
    "CC57.Bin_BRight_Full": (1,56),

    "CC58.Bin_BLeft_Full": (0,57),
    "CC58.Bin_BRight_Full": (1,57),

    "CC59.Bin_BLeft_Full": (0,58),
    "CC59.Bin_BRight_Full": (1,58),

    "CC60.Bin_BLeft_Full": (0,59),
    "CC60.Bin_BRight_Full": (1,59),

    "CC61.Bin_BLeft_Full": (0,60),
    "CC61.Bin_BRight_Full": (1,60),

    "CC62.Bin_BLeft_Full": (0,61),
    "CC62.Bin_BRight_Full": (1,61),

    "CC63.Bin_BLeft_Full": (0,62),
    "CC63.Bin_BRight_Full": (1,62),

    "CC64.Bin_BLeft_Full": (0,63),
    "CC64.Bin_BRight_Full": (1,63),

    "CC65.Bin_BLeft_Full": (0,64),
    "CC65.Bin_BRight_Full": (1,64),

    "CC66.Bin_BLeft_Full": (0,65),
    "CC66.Bin_BRight_Full": (1,65),

    "CC67.Bin_BLeft_Full": (0,66),
    "CC67.Bin_BRight_Full": (1,66),

    "CC68.Bin_BLeft_Full": (0,67),
    "CC68.Bin_BRight_Full": (1,67),

    "CC69.Bin_BLeft_Full": (0,68),
    "CC69.Bin_BRight_Full": (1,68),

    "CC70.Bin_BLeft_Full": (0,69),
    "CC70.Bin_BRight_Full": (1,69),

    "CC71.Bin_BLeft_Full": (0,70),
    "CC71.Bin_BRight_Full": (1,70),

    "CC72.Bin_BLeft_Full": (0,71),
    "CC72.Bin_BRight_Full": (1,71),

    "CC73.Bin_BLeft_Full": (0,72),
    "CC73.Bin_BRight_Full": (1,72),

    "CC74.Bin_BLeft_Full": (0,73),
    "CC74.Bin_BRight_Full": (1,73),

    "CC75.Bin_BLeft_Full": (0,74),
    "CC75.Bin_BRight_Full": (1,74),

    "CC76.Bin_BLeft_Full": (0,75),
    "CC76.Bin_BRight_Full": (1,75),

    "CC77.Bin_BLeft_Full": (0,76),
    "CC77.Bin_BRight_Full": (1,76)

}

rows = 2
cols = 77
table_df = pd.DataFrame("", index=range(rows), columns=range(cols), dtype=object)

trigger_values = {}
for alarm_id, trigger in trigger_counts.items():
    if alarm_id in row_col_mapping:
        row, col = row_col_mapping[alarm_id]
        trigger_values[(row, col)] = trigger

table_df.index = ['Bin_BLeft_Full', 'Bin_BRight_Full']
table_df.columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77']

min_count = 0 
max_count = max(trigger_values.values())

norm = mcolors.Normalize(vmin=min_count, vmax=max_count)
cmap = plt.colormaps.get_cmap("gnuplot2_r")

cell_colours = np.full((rows, cols), '#FFFFFF')
for (row, col), count in trigger_values.items():
    color = cmap(norm(count))
    cell_colours[row, col] = mcolors.to_hex(color)

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

tbl = table(ax, table_df, loc='center', colWidths=[0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02])


tbl.auto_set_font_size(False)
tbl.set_fontsize(7)
tbl.scale(0.7, 0.7)

for (i, j), cell in tbl.get_celld().items():
    i = i - 1
    if (i, j) in trigger_values:
        cell.set_facecolor(cell_colours[i, j])
    else:
        cell.set_facecolor('#FFFFFF')
    cell.set_edgecolor('black')

cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.02])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax, label='Trigger Counts', orientation='horizontal')

cbar.set_ticks([min_count, (max_count/10), (2*max_count/10), (3*max_count/10), (4*max_count/10), (5*max_count/10), (6*max_count/10), (7*max_count/10), (8*max_count/10), (9*max_count/10), max_count])
cbar.set_ticklabels([min_count, float(max_count/10), 2*max_count/10, 3*max_count/10, 4*max_count/10, 5*max_count/10, 6*max_count/10, 7*max_count/10, 8*max_count/10, 9*max_count/10, max_count])

plt.show()