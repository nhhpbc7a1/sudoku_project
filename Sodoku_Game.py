import matplotlib.pyplot as plt
import numpy as np

# Create a blank 9x9 grid
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xticks(np.arange(0, 9, 1))
ax.set_yticks(np.arange(0, 9, 1))

# Draw the thinner grid lines for each cell
ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)

# Highlight the 3x3 subgrid boundaries with thicker lines
for i in range(0, 10, 3):
    ax.axhline(i, color='black', linewidth=2)
    ax.axvline(i, color='black', linewidth=2)

# Set the ticks and labels for columns and rows
ax.set_xticks(np.arange(0.5, 9.5, 1), minor=True)
ax.set_yticks(np.arange(0.5, 9.5, 1), minor=True)
ax.tick_params(which='minor', size=0)

# Hide major ticks
ax.tick_params(which='major', bottom=False, left=False)

# Example row and column labels (like in your image)
for i, label in enumerate(['1', '2', '3'], start=1):
    ax.text(i-1, 9.5, label, ha='center', va='center', fontsize=14)

# Remove ticks and labels for a cleaner look
ax.set_xticklabels([])
ax.set_yticklabels([])

# Adjust plot limits
ax.set_xlim(-0.5, 8.5)
ax.set_ylim(-0.5, 8.5)

# Display the grid
plt.gca().invert_yaxis()
plt.show()