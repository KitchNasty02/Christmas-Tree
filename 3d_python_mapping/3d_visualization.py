import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def visualize(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(xs, ys, zs, c=zs, cmap='viridis', s=20)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_title("3D LED Tree Mapping")
    plt.show()


if __name__ == "__main__":
    # Example load from numpy or json
    points = np.load(r"C:\Users\conno\OneDrive\Desktop\Projects\Christmas Tree\Led Mapping (Arduino)\include\led_positions.h")
    visualize(points)
