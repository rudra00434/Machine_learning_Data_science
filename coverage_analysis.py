import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load AP coordinates
data = np.loadtxt("AP_COR_35.txt")
if data.shape[1] == 2:
    x = data[:, 0]
    y = data[:, 1]
else:
    x = data[0]
    y = data[1]

# Coverage parameters
coverage_radius = 130  # Increased to cover all edges
area_x, area_y = 300, 300

# Create coverage heatmap
grid_x, grid_y = np.meshgrid(np.linspace(0, area_x, 300), np.linspace(0, area_y, 300))
coverage = np.zeros_like(grid_x)

# Calculate coverage at each grid point
for i in range(len(x)):
    distance = np.sqrt((grid_x - x[i])**2 + (grid_y - y[i])**2)
    coverage[distance <= coverage_radius] = 1

covered_percent = (np.sum(coverage) / coverage.size) * 100

# Plot
fig, ax = plt.subplots(figsize=(12, 11), dpi=100)

# Show coverage
im = ax.contourf(grid_x, grid_y, coverage, levels=[0, 0.5, 1], colors=['white', '#90EE90'], alpha=0.8)

# Overlay APs
ax.scatter(x, y, s=100, color='blue', zorder=5, edgecolor='darkblue', linewidth=2, label='Access Point')

# Coverage circles
for i in range(len(x)):
    circle = plt.Circle((x[i], y[i]), coverage_radius, fill=False, edgecolor='green', linewidth=1.5, alpha=0.6)
    ax.add_patch(circle)

# Mark uncovered areas
ax.text(10, 10, '⚠ Check edges!', fontsize=14, color='red', fontweight='bold', 
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

ax.set_xlim(0, area_x)
ax.set_ylim(0, area_y)
ax.set_xlabel("X (meters)", fontsize=14, fontweight='bold')
ax.set_ylabel("Y (meters)", fontsize=14, fontweight='bold')
ax.set_title(f"Coverage Analysis: {covered_percent:.1f}% of area covered (Radius={coverage_radius}m)", 
             fontsize=15, fontweight='bold', pad=20)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig("coverage_analysis.pdf", format='pdf', bbox_inches='tight')
plt.savefig("coverage_analysis.png", dpi=150, bbox_inches='tight')
print(f"\nCoverage Analysis: {covered_percent:.1f}% of area is covered with radius {coverage_radius}m")
print(f"Uncovered areas: {100-covered_percent:.1f}%")
print("\nTo cover edge areas, we need to increase the radius or reposition APs.")
