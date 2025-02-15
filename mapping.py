import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Example data dictionary: {(lane, location): downtime}
data = {
    (1, 1): 10, (1, 2): 50, (1, 3): 90,
    (2, 1): 20, (2, 2): 60, (2, 3): 80,
    (3, 1): 15, (3, 2): 40, (3, 3): 70,
    # Add more entries for lanes 4–8
}

# Define grid dimensions
num_lanes = 8
num_columns = 10  # Adjust as needed
grid = np.zeros((num_lanes, num_columns))  # Default grid with zeros

# Populate the grid with downtime values
for (lane, loc), downtime in data.items():
    grid[lane - 1, loc - 1] = downtime  # Adjust for 0-based indexing

# Create a colormap (green to red)
cmap = mcolors.LinearSegmentedColormap.from_list("downtime_map", ["green", "yellow", "red"])
norm = mcolors.Normalize(vmin=0, vmax=100)  # Normalize downtime values between 0 and 100

# Plot the grid
fig, ax = plt.subplots(figsize=(10, 8))
c = ax.pcolormesh(grid, cmap=cmap, edgecolors='k', linewidth=0.5, norm=norm)

# Add labels
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        value = grid[i, j]
        if value > 0:  # Label only non-zero cells
            ax.text(j + 0.5, i + 0.5, f"{int(value)}", color="black",
                    ha="center", va="center", fontsize=8)

# Customize the layout
plt.colorbar(c, ax=ax, label="Downtime (minutes)")
plt.title("Photoeye Downtime Heatmap")
plt.tight_layout()
plt.show()
