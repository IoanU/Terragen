from __future__ import annotations
import numpy as np
from ..rng import make_rng
from ..registry import register_noise

@register_noise("diamond_square2d")
class DiamondSquare2D:
    def __init__(self, seed: int, size: int = 257, roughness: float = 0.5):
        self.size = size
        self.roughness = roughness
        self.rng = make_rng(seed)

    def sample(self) -> np.ndarray:
        n = self.size
        hm = np.zeros((n, n), dtype=np.float32)
        hm[0, 0] = self.rng.random(); hm[0, -1] = self.rng.random()
        hm[-1, 0] = self.rng.random(); hm[-1, -1] = self.rng.random()
        step = n - 1; scale = self.roughness
        while step > 1:
            half = step // 2
            # diamond
            for y in range(half, n - 1, step):
                for x in range(half, n - 1, step):
                    avg = (hm[y-half, x-half] + hm[y-half, x+half] +
                           hm[y+half, x-half] + hm[y+half, x+half]) * 0.25
                    hm[y, x] = np.clip(avg + (self.rng.random()*2-1)*scale, 0.0, 1.0)
            # square
            for y in range(0, n, half):
                for x in range((y + half) % step, n, step):
                    vals = []
                    if y-half >= 0: vals.append(hm[y-half, x])
                    if y+half < n: vals.append(hm[y+half, x])
                    if x-half >= 0: vals.append(hm[y, x-half])
                    if x+half < n: vals.append(hm[y, x+half])
                    avg = np.mean(vals)
                    hm[y, x] = np.clip(avg + (self.rng.random()*2-1)*scale, 0.0, 1.0)
            step //= 2; scale *= self.roughness
        hm = (hm - hm.min()) / (hm.max() - hm.min() + 1e-9)
        return hm
