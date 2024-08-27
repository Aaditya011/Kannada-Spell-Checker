import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ["Completely Misspelled Words", "Invalid Root with Valid Suffix"]
top1 = [40.0, 16.67]
top5 = [70.0, 50.0]
top8 = [70.0, 83.33]

# Position of the bars on the x-axis
x = np.arange(len(categories))

# Width of each bar
width = 0.2

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Grouped bars
ax.bar(x - width, top1, width, label="Top 1 candidate", color='steelblue')
ax.bar(x, top5, width, label="Top 5 candidates", color='indianred')
ax.bar(x + width, top8, width, label="Top 8 candidates", color='darkorange')

# Set labels and title
ax.set_xlabel("Error Type")
ax.set_ylabel("Accuracy (%)")
ax.set_title("Accuracy Rates for Different Error Types")
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_ylim(0, 100)
ax.legend()

# Display the plot
plt.show()
