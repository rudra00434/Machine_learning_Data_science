import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Load coordinates from file ────────────────────────────────────────────
data = np.loadtxt("AP_COR_35.txt")

# Handle both possible file layouts:
#   Layout A → 2 rows × 25 cols  (row 0 = X, row 1 = Y)
#   Layout B → 25 rows × 2 cols  (col 0 = X, col 1 = Y)
if data.ndim == 1:
    x = data[:len(data)//2]
    y = data[len(data)//2:]
elif data.shape[0] == 2:
    x = data[0]
    y = data[1]
elif data.shape[1] == 2:
    x = data[:, 0]
    y = data[:, 1]
else:
    raise ValueError(f"Unexpected data shape: {data.shape}")

num_APs         = len(x)
area_size       = 300
coverage_radius = 130      # ← increased to cover all edges (no white gaps)

print(f"Loaded {num_APs} access points from file.")

# ── Plot ──────────────────────────────────────────────────────────────────
# Larger figure for publication quality (fills space like journal images)
fig, ax = plt.subplots(figsize=(12, 11), dpi=100)

# ── Coverage circles (drawn first, behind everything) ─────────────────────
for i in range(num_APs):
    # Filled circle (very light)
    filled = plt.Circle(
        (x[i], y[i]),
        coverage_radius,
        color="#17D61E",
        alpha=0.08,          # very transparent fill — avoids dark overlap mess
        linewidth=0
    )
    # Edge-only circle (solid border)
    border = plt.Circle(
        (x[i], y[i]),
        coverage_radius,
        fill=False,
        edgecolor='#2E7D32',
        linewidth=0.9,
        alpha=0.5
    )
    ax.add_patch(filled)
    ax.add_patch(border)

# ── AP scatter points ─────────────────────────────────────────────────────
ax.scatter(x, y, s=80, color='blue', zorder=5, label="Access Point")

# ── AP labels ────────────────────────────────────────────────────────────
for i in range(num_APs):
    ax.annotate(
        f"AP{i+1}",
        xy=(x[i], y[i]),
        xytext=(5, 6),
        textcoords='offset points',
        fontsize=7.5,
        color='darkblue',
        zorder=6
    )

# ── Axes & cosmetics ──────────────────────────────────────────────────────
ax.set_xlim(0, area_size)
ax.set_ylim(0, area_size)
ax.set_xlabel("X (meters)", fontsize=14, fontweight='bold')
ax.set_ylabel("Y (meters)", fontsize=14, fontweight='bold')
ax.set_title(
    f"Distribution of {num_APs} Access Points in a {area_size}m × {area_size}m Area",
    fontsize=15, fontweight='bold', pad=20
)
ax.set_aspect('equal', adjustable='box')
ax.grid(True, linestyle='--', alpha=0.3, color='gray')

# ── Legend ────────────────────────────────────────────────────────────────
blue_dot   = mpatches.Patch(color='blue',    label='Access Point')
green_ring = mpatches.Patch(facecolor='#4CAF50', edgecolor='#2E7D32',
                             alpha=0.4,
                             label=f'Coverage radius = {coverage_radius} m')
ax.legend(handles=[blue_dot, green_ring], loc='upper right', fontsize=11, framealpha=0.95, edgecolor='black', fancybox=True)

# ── Info text below figure ────────────────────────────────────────────────


plt.tight_layout(rect=[0, 0.04, 1, 0.98])
# ── Save for LaTeX (PDF is best—vector-based & smaller) ──────────────────
plt.savefig("AP_distribution_2.pdf", format='pdf', bbox_inches='tight', pad_inches=0.2)
# ── Alternative: Optimized PNG (if PDF not needed) ──────────────────────
plt.savefig("AP_distribution_2.png", dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none', pad_inches=0.2)
plt.show()
