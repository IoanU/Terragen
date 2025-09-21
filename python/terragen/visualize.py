import matplotlib.pyplot as plt
import numpy as np

def show_heightmap(h: np.ndarray):
    plt.figure()
    plt.imshow(h, cmap="gray", origin="lower")
    plt.title("Terrain heightmap")
    plt.colorbar()
    plt.show()
