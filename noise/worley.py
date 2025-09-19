from __future__ import annotations
import numpy as np
from ..rng import make_rng
from ..registry import register_noise

@register_noise("worley2d")
class Worley2D:
    def __init__(self, seed: int, cells: int = 32, metric: str = "euclid"):
        self.cells = cells
        self.metric = metric
        rng = make_rng(seed)
        self.fx = rng.random((cells, cells))
        self.fy = rng.random((cells, cells))
    def sample(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        X = x * self.cells
        Y = y * self.cells
        xi = np.floor(X).astype(int) % self.cells
        yi = np.floor(Y).astype(int) % self.cells
        h, w = x.shape
        out = np.empty_like(x, dtype=np.float32)
        for i in range(h):
            for j in range(w):
                cx = xi[i, j]; cy = yi[i, j]
                min_d = 1e9
                for oy in (-1, 0, 1):
                    for ox in (-1, 0, 1):
                        gx = (cx + ox) % self.cells
                        gy = (cy + oy) % self.cells
                        px = gx + self.fx[gy, gx]
                        py = gy + self.fy[gy, gx]
                        dx = X[i, j] - px
                        dy = Y[i, j] - py
                        if self.metric == "euclid":
                            d = dx*dx + dy*dy
                        elif self.metric == "manhattan":
                            d = abs(dx) + abs(dy)
                        else:
                            d = max(abs(dx), abs(dy))
                        if d < min_d: min_d = d
                out[i, j] = min_d
        out = (out - out.min()) / (out.max() - out.min() + 1e-9)
        return 1.0 - out
