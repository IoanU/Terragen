from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def save_png(hmap: np.ndarray, path: str, cmap: str = "gray"):
    dpi = 150
    h, w = hmap.shape
    fig = plt.figure(frameon=False)
    fig.set_size_inches(w / dpi, h / dpi)
    ax = plt.Axes(fig, [0, 0, 1, 1])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(hmap, cmap=cmap, interpolation="nearest")
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
