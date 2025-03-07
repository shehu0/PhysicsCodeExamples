import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grid size
GRID_SIZE = 20
ITERATIONS = 1000

# Set up the figure
fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(12, 6), gridspec_kw={"width_ratios": [1, 1]}
)

# Initialize grid with 1 quantum per site
grid = np.ones((GRID_SIZE, GRID_SIZE), dtype=int)


def update(frame):
    global grid

    # Select two random sites
    x1, y1 = np.random.randint(0, GRID_SIZE, size=2)
    x2, y2 = np.random.randint(0, GRID_SIZE, size=2)

    # Transfer energy if possible
    if grid[x1, y1] > 0:
        grid[x1, y1] -= 1
        grid[x2, y2] += 1

    # Update grid visualization
    ax1.clear()
    ax1.imshow(grid, cmap="inferno", origin="upper")
    ax1.set_title("Energy Distribution Grid")

    # Compute histogram
    energy_levels, counts = np.unique(grid, return_counts=True)

    ax2.clear()
    ax2.bar(energy_levels, counts, color="blue", edgecolor="black")
    ax2.set_xlabel("Energy Quanta")
    ax2.set_ylabel("Number of Sites")
    ax2.set_title("Energy Distribution Histogram")
    ax2.set_xlim(0, np.max(grid) + 1)


def init():
    ax1.imshow(grid, cmap="inferno", origin="upper")
    ax1.set_title("Energy Distribution Grid")

    energy_levels, counts = np.unique(grid, return_counts=True)
    ax2.bar(energy_levels, counts, color="blue", edgecolor="black")
    ax2.set_xlabel("Energy Quanta")
    ax2.set_ylabel("Number of Sites")
    ax2.set_title("Energy Distribution Histogram")
    ax2.set_xlim(0, np.max(grid) + 1)


ani = animation.FuncAnimation(
    fig, update, frames=ITERATIONS, interval=50, repeat=False, init_func=init
)
plt.show()
