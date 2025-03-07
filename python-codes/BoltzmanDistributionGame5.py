# press key 'p' to pause the animation at any time
# press again to unpause

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grid size
GRID_SIZE = 20
ITERATIONS = 1000

PAUSE_FRAMES = 40  # Number of frames to pause on the initial state
PAUSE_AFTER_FIRST_ITERATION = 40  # Number of frames to pause after the first iteration


# Initialize grids
grid1 = np.ones((GRID_SIZE, GRID_SIZE), dtype=int)  # First grid with 1 quantum per site
grid2 = 2 * np.ones(
    (GRID_SIZE, GRID_SIZE), dtype=int
)  # Second grid with 2 quanta per site

# Set up the figure and axes
fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3, figsize=(18, 6)
)  # Single row with three columns
cbar1 = None  # Placeholder for the color bar of the first grid
cbar2 = None  # Placeholder for the color bar of the second grid

# First grid visualization
img1 = ax1.imshow(grid1, cmap="inferno", origin="upper")
cbar1 = fig.colorbar(img1, ax=ax1)
cbar1.set_label("Quanta per Site (Grid 1)")

# Second grid visualization
img2 = ax2.imshow(grid2, cmap="viridis", origin="upper")
cbar2 = fig.colorbar(img2, ax=ax2)
cbar2.set_label("Quanta per Site (Grid 2)")

# Variable to control the pause state
paused = False
first_iteration_complete = False  # Track if the first iteration is complete
pause_counter = 0  # Counter for the pause after the first iteration


# Function to handle key press events
def on_key(event):
    global paused
    if event.key == "p":  # Use 'p' key to pause/unpause
        paused = not paused
        print(f"Animation paused: {paused}")  # Debugging output


# Connect the key press event to the handler
fig.canvas.mpl_connect("key_press_event", on_key)


def update(frame):
    global \
        grid1, \
        grid2, \
        img1, \
        img2, \
        cbar1, \
        cbar2, \
        paused, \
        first_iteration_complete, \
        pause_counter

    if paused:
        return  # Do nothing if paused

    if frame < PAUSE_FRAMES:
        return  # Pause on the initial state

    # Check if the first iteration is complete and pause for 40 frames
    if not first_iteration_complete and frame >= PAUSE_FRAMES + ITERATIONS:
        first_iteration_complete = True
        pause_counter = 0

    if first_iteration_complete and pause_counter < PAUSE_AFTER_FIRST_ITERATION:
        pause_counter += 1
        return  # Pause for 40 frames after the first iteration

    # Update Grid 1
    x1, y1 = np.random.randint(0, GRID_SIZE, size=2)
    x2, y2 = np.random.randint(0, GRID_SIZE, size=2)
    if grid1[x1, y1] > 0:
        grid1[x1, y1] -= 1
        grid1[x2, y2] += 1

    # Update Grid 2
    x1, y1 = np.random.randint(0, GRID_SIZE, size=2)
    x2, y2 = np.random.randint(0, GRID_SIZE, size=2)
    if grid2[x1, y1] > 0:
        grid2[x1, y1] -= 1
        grid2[x2, y2] += 1

    # Update grid visualizations
    img1.set_data(grid1)
    img1.set_clim(vmin=0, vmax=np.max(grid1))  # Update color scale for Grid 1
    cbar1.update_normal(img1)

    img2.set_data(grid2)
    img2.set_clim(vmin=0, vmax=np.max(grid2))  # Update color scale for Grid 2
    cbar2.update_normal(img2)

    ax1.set_title("Energy Distribution Grid 1 (1 Quanta Initial)")
    ax2.set_title("Energy Distribution Grid 2 (2 Quanta Initial)")

    # Compute histograms
    energy_levels1, counts1 = np.unique(grid1, return_counts=True)
    energy_levels2, counts2 = np.unique(grid2, return_counts=True)

    # Plot combined histogram
    ax3.clear()
    ax3.bar(energy_levels1, counts1, color="blue", edgecolor="black", label="Grid 1")
    ax3.bar(
        energy_levels2,
        counts2,
        color="orange",
        edgecolor="black",
        alpha=0.5,
        label="Grid 2",
    )
    ax3.set_xlabel("Energy Quanta")
    ax3.set_ylabel("Number of Sites")
    ax3.set_title("Energy Distribution Histogram")
    ax3.set_xlim(0, max(np.max(grid1), np.max(grid2)) + 1)
    ax3.legend()


def init():
    img1.set_data(grid1)
    img1.set_clim(vmin=0, vmax=np.max(grid1))
    cbar1.update_normal(img1)

    img2.set_data(grid2)
    img2.set_clim(vmin=0, vmax=np.max(grid2))
    cbar2.update_normal(img2)

    ax1.set_title("Energy Distribution Grid 1 (1 Quanta Initial)")
    ax2.set_title("Energy Distribution Grid 2 (2 Quanta Initial)")

    energy_levels1, counts1 = np.unique(grid1, return_counts=True)
    energy_levels2, counts2 = np.unique(grid2, return_counts=True)

    ax3.bar(energy_levels1, counts1, color="blue", edgecolor="black", label="Grid 1")
    ax3.bar(
        energy_levels2,
        counts2,
        color="orange",
        edgecolor="black",
        alpha=0.5,
        label="Grid 2",
    )
    ax3.set_xlabel("Energy Quanta")
    ax3.set_ylabel("Number of Sites")
    ax3.set_title("Energy Distribution Histogram")
    ax3.set_xlim(0, max(np.max(grid1), np.max(grid2)) + 1)
    ax3.legend()


ani = animation.FuncAnimation(
    fig,
    update,
    frames=ITERATIONS + PAUSE_FRAMES + PAUSE_AFTER_FIRST_ITERATION,
    interval=50,
    repeat=False,
    init_func=init,
)

# Ensure the figure is focused to capture key events
plt.show()
