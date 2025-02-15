import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import table
import matplotlib.colors as mcolors
import matplotlib as mpl

# Sample data stored as a dictionary (time in HH:MM:SS format)
data = {
    "Singulator_U1U2_Jam": "00:00:10",
    "MG4_PHTEYE_JAM": "00:02:45",
    "MCP_ESTOP_NOTRESET": "00:01:20",
    "VIS_MTRX_BED_BLT_FLT": "00:06:35",
    "G1_PHTEYE_JAM": "00:03:10",
    "G9_PHTEYE_JAM": "00:09:20",
}

# Manual mapping of alarm_id to row and column
row_mapping = {
    "Singulator_U1U2_Jam": 0,
    "MG4_PHTEYE_JAM": 0,
    "MCP_ESTOP_NOTRESET": 0,
    "VIS_MTRX_BED_BLT_FLT": 0,
    "G1_PHTEYE_JAM": 0,
    "G9_PHTEYE_JAM": 0,
}

col_mapping = {
    "Singulator_U1U2_Jam": 0,
    "MG4_PHTEYE_JAM": 1,
    "MCP_ESTOP_NOTRESET": 2,
    "VIS_MTRX_BED_BLT_FLT": 3,
    "G1_PHTEYE_JAM": 4,
    "G9_PHTEYE_JAM": 5,
}

# Function to convert time string "HH:MM:SS" to seconds
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

# Function to convert seconds to "HH:MM:SS" format
def seconds_to_hms(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Create an empty DataFrame with appropriate size and dtype=object
rows = 8
cols = 8
table_df = pd.DataFrame("", index=range(rows), columns=range(cols), dtype=object)

# Populate the DataFrame based on the mappings
time_values = {}
for alarm_id, total_time in data.items():
    if alarm_id in row_mapping and alarm_id in col_mapping:
        row = row_mapping[alarm_id]
        col = col_mapping[alarm_id]
        table_df.loc[row, col] = ""
        time_values[(row, col)] = time_to_seconds(total_time)

# Set custom row and column labels
table_df.index = ['Strand 1', 'Strand 2', 'Strand 3', 'Strand 4', 'Strand 5', 'Strand 6', 'Strand 7', 'Strand 8']  # Row titles (you can customize this)
# table_df.columns = ['D0', 'D1', 'D2', 'D3', 'D4', 'D5']  # Column titles (you can customize this)

# table_df.index = ['Strand 1']  # Row titles (you can customize this)
table_df.columns = ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'F1', 'F2']  # Column titles (you can customize this)

# Get absolute time range for color mapping (in seconds)
min_time = 0  # Set minimum time to 0 seconds (00:00:00)
max_time = 600  # Set maximum time to 24 hours in seconds (24:00:00)
norm = mcolors.Normalize(vmin=min_time, vmax=max_time)
cmap = plt.colormaps.get_cmap("gnuplot2_r")  # Use the reversed colormap (RdYlGn_r)

# Create cell colours based on time values, directly apply color map to the absolute time
cell_colours = np.full((rows, cols), '#FFFFFF')  # 1a9850 if RdYlGn_r cmap
for (row, col), time_sec in time_values.items():
    color = cmap(norm(time_sec))  # Get color for the current time value
    cell_colours[row, col] = mcolors.to_hex(color)  # Convert to hex

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# Create the table with no numbers, just colors
tbl = table(ax, table_df, loc='center', colWidths=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05], cellColours=cell_colours)

tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1)

# Add a colorbar on the right to indicate the time range
cbar_ax = fig.add_axes([0.85, 0.1, 0.03, 0.8])  # Position the colorbar on the right
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Empty array for ScalarMappable
cbar = fig.colorbar(sm, cax=cbar_ax, label='Time (HH:MM:SS)', orientation='vertical')

# Customizing the ticks on the colorbar
cbar.set_ticks([0, 200, 400, 600])  # Set ticks for 0, 12:00:00, and 24:00:00
cbar.set_ticklabels([seconds_to_hms(0), seconds_to_hms(200), seconds_to_hms(400), seconds_to_hms(600)])  # Format ticks as HH:MM:SS

# Show the table
plt.show()