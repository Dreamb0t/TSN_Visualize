import matplotlib.pyplot as plt
import numpy as np

# Define tasks and their positions
tasks = ["ES1, SW1", "ES2, SW1", "SW1, ES3"]
task_positions = {tasks[i]: i for i in range(len(tasks))}

# Time segments (start, width, y position, value, color)
blocks = [
    (5, 7, "ES1, SW1", 1.1, "blue"),
    (13.24, 7.1, "ES1, SW1", 7.1, "blue"),
    (23.98, 3.1, "ES1, SW1", 3.1, "green"),
    (36, 5.1, "ES1, SW1", 5.1, "red"),
    
    (6.8, 8.1, "ES2, SW1", 8.1, "blue"),
    (18, 2.1, "ES2, SW1", 2.1, "green"),
    (28.74, 6.1, "ES2, SW1", 6.1, "blue"),
    (48, 4.1, "ES2, SW1", 4.1, "green"),

    (12, 1.1, "SW1, ES3", 1.1, "green"),
    (30, 2.1, "SW1, ES3", 2.1, "green"),
    (48, 3.1, "SW1, ES3", 3.1, "green"),
    (66, 4.1, "SW1, ES3", 4.1, "green"),
    (89.98, 8.1, "SW1, ES3", 8.1, "blue"),
    (107.63, 7.1, "SW1, ES3", 7.1, "blue"),
    (125.28, 6.1, "SW1, ES3", 6.1, "blue"),
    (138.52, 5.1, "SW1, ES3", 5.1, "red"),
]

fig, ax = plt.subplots(figsize=(12, 4))

# Plot the timing blocks
for start, duration, task, value, color in blocks:
    y_pos = task_positions[task]
    ax.barh(y_pos, duration, left=start, height=0.5, color=color, edgecolor="black", alpha=0.7)
    ax.text(start + duration / 2, y_pos, str(value), ha='center', va='center', fontsize=10, color="black", fontweight='bold')

# Connect blocks with lines
connections = [
    (5, "ES1, SW1", 6.8, "ES2, SW1"),
    (12, "SW1, ES3", 18, "ES2, SW1"),
    (30, "SW1, ES3", 36, "ES1, SW1"),
    (66, "SW1, ES3", 89.98, "SW1, ES3"),
    (138.52, "SW1, ES3", 151.76, "SW1, ES3")
]

for start, task_start, end, task_end in connections:
    y1, y2 = task_positions[task_start], task_positions[task_end]
    ax.plot([start, end], [y1, y2], color="red", linewidth=1.5, marker='o')

# Labels and grid
ax.set_yticks(range(len(tasks)))
ax.set_yticklabels(tasks)
ax.set_xticks(np.arange(0, 160, 10))
ax.set_xlabel("Time (µs)")
ax.set_title("Timing Diagram Representation")
ax.grid(True, linestyle="--", alpha=0.5)

plt.show()
