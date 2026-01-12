import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Step 1: Load your 3D positions --- #
filename = r"arduino_platformio\include\led_positions_3D.h"

positions = []

with open(filename, "r") as f:
    for line in f:
        # match lines like: { -0.061680f, -0.232108f, 0.656597f },
        m = re.match(r"\s*\{\s*([-0-9.e]+)f,\s*([-0-9.e]+)f,\s*([-0-9.e]+)f\s*\}", line)
        if m:
            x, y, z = map(float, m.groups())
            if x != -999:  # skip missing LEDs
                positions.append((x, y, z))

# convert to separate lists
xs, ys, zs = zip(*positions)

# --- Step 2: Create 3D scatter plot --- #
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs, ys, zs, c='red', s=50)

# optional: label axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_title('LED 3D Positions')

# optional: set equal aspect ratio
ax.set_box_aspect([1,1,1])

plt.show()
