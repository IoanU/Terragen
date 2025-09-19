from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def show_1d(line: np.ndarray, title: str = "1D Terrain"):
    plt.figure()
    plt.plot(line)
    plt.fill_between(range(len(line)), line, 0)
    plt.title(title)
    plt.show()

def show_2d(hmap: np.ndarray, title: str = "2D Heightmap"):
    plt.figure()
    plt.imshow(hmap, cmap="gray", interpolation="nearest")
    plt.title(title)
    plt.axis("off")
    plt.show()
