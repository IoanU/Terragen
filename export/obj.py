from __future__ import annotations
import numpy as np

def save_obj(hmap: np.ndarray, path: str, vertical_scale: float = 60.0):
    h, w = hmap.shape
    zs = (hmap * vertical_scale).astype(float)
    with open(path, "w") as f:
        for y in range(h):
            for x in range(w):
                f.write(f"v {x} {zs[y, x]} {y}\n")
        def idx(x, y): return y * w + x + 1
        for y in range(h - 1):
            for x in range(w - 1):
                v1 = idx(x, y); v2 = idx(x+1, y); v3 = idx(x+1, y+1); v4 = idx(x, y+1)
                f.write(f"f {v1} {v2} {v3}\n")
                f.write(f"f {v1} {v3} {v4}\n")
