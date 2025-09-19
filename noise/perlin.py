from __future__ import annotations
import numpy as np
from .base import PermTable, fade, lerp
from ..registry import register_noise

def _grad(h, x, y=0.0, z=0.0):
    h &= 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h in (12, 14) else z)
    return ((u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v))

@register_noise("perlin1d")
class Perlin1D:
    def __init__(self, seed: int):
        self.perm = PermTable.build(seed).p
    def sample(self, x: np.ndarray) -> np.ndarray:
        xi = np.floor(x).astype(int) & 255
        xf = x - np.floor(x)
        u = fade(xf)
        a = self.perm[xi]
        b = self.perm[(xi + 1) & 255]
        n0 = _grad(self.perm[a], xf)
        n1 = _grad(self.perm[b], xf - 1)
        return lerp(n0, n1, u)

@register_noise("perlin2d")
class Perlin2D:
    def __init__(self, seed: int):
        self.perm = PermTable.build(seed).p
    def sample(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        xi = (np.floor(x).astype(int)) & 255
        yi = (np.floor(y).astype(int)) & 255
        xf = x - np.floor(x)
        yf = y - np.floor(y)
        u = fade(xf); v = fade(yf)
        A = self.perm[xi] + yi
        B = self.perm[(xi + 1) & 255] + yi
        n00 = _grad(self.perm[A], xf, yf)
        n01 = _grad(self.perm[A + 1], xf, yf - 1)
        n10 = _grad(self.perm[B], xf - 1, yf)
        n11 = _grad(self.perm[B + 1], xf - 1, yf - 1)
        x1 = lerp(n00, n10, u); x2 = lerp(n01, n11, u)
        return lerp(x1, x2, v)
