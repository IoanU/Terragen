# terragen/noise/perlin.py
from __future__ import annotations
import numpy as np
from .base import PermTable, fade, lerp
from ..registry import register_noise

def _grad1d(h: np.ndarray, x: np.ndarray) -> np.ndarray:
    # For 1D Perlin, gradient is just +x or -x depending on hash parity
    return np.where((h & 1) == 0, x, -x)

def _grad_nd(h: np.ndarray, x: np.ndarray, y: np.ndarray, z: np.ndarray | float = 0.0) -> np.ndarray:
    # Vectorized n-dim gradient selection (works for 2D/3D)
    h = h & 15
    u = np.where(h < 8, x, y)
    v = np.where(h < 4, y, np.where((h == 12) | (h == 14), x, z))
    return np.where((h & 1) == 0, u, -u) + np.where((h & 2) == 0, v, -v)

@register_noise("perlin1d")
class Perlin1D:
    def __init__(self, seed: int):
        self.perm = PermTable.build(seed).p  # shape (512,)

    def sample(self, x: np.ndarray) -> np.ndarray:
        # x can be vector; compute floor and frac parts
        xi = np.floor(x).astype(np.int32) & 255
        xf = x - np.floor(x)
        u = fade(xf)

        a = self.perm[xi]                  # hash at lattice i
        b = self.perm[(xi + 1) & 255]      # hash at lattice i+1

        n0 = _grad1d(a, xf)
        n1 = _grad1d(b, xf - 1.0)
        return lerp(n0, n1, u)

@register_noise("perlin2d")
class Perlin2D:
    def __init__(self, seed: int):
        self.perm = PermTable.build(seed).p

    def sample(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        xi = (np.floor(x).astype(np.int32)) & 255
        yi = (np.floor(y).astype(np.int32)) & 255
        xf = x - np.floor(x)
        yf = y - np.floor(y)
        u = fade(xf); v = fade(yf)

        A  = self.perm[xi] + yi
        B  = self.perm[(xi + 1) & 255] + yi

        n00 = _grad_nd(self.perm[A],     xf,     yf, 0.0)
        n01 = _grad_nd(self.perm[A + 1], xf,     yf-1.0, 0.0)
        n10 = _grad_nd(self.perm[B],     xf-1.0, yf, 0.0)
        n11 = _grad_nd(self.perm[B + 1], xf-1.0, yf-1.0, 0.0)

        x1 = lerp(n00, n10, u)
        x2 = lerp(n01, n11, u)
        return lerp(x1, x2, v)

@register_noise("perlin3d")
class Perlin3D:
    def __init__(self, seed: int):
        self.perm = PermTable.build(seed).p

    def sample(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
        xi = (np.floor(x).astype(np.int32)) & 255
        yi = (np.floor(y).astype(np.int32)) & 255
        zi = (np.floor(z).astype(np.int32)) & 255
        xf = x - np.floor(x);  yf = y - np.floor(y);  zf = z - np.floor(z)
        u = fade(xf); v = fade(yf); w = fade(zf)

        A  = self.perm[xi] + yi
        AA = self.perm[A] + zi
        AB = self.perm[A + 1] + zi
        B  = self.perm[(xi + 1) & 255] + yi
        BA = self.perm[B] + zi
        BB = self.perm[B + 1] + zi

        n000 = _grad_nd(self.perm[AA],     xf,     yf,     zf)
        n001 = _grad_nd(self.perm[AA + 1], xf,     yf,     zf-1.0)
        n010 = _grad_nd(self.perm[AB],     xf,     yf-1.0, zf)
        n011 = _grad_nd(self.perm[AB + 1], xf,     yf-1.0, zf-1.0)
        n100 = _grad_nd(self.perm[BA],     xf-1.0, yf,     zf)
        n101 = _grad_nd(self.perm[BA + 1], xf-1.0, yf,     zf-1.0)
        n110 = _grad_nd(self.perm[BB],     xf-1.0, yf-1.0, zf)
        n111 = _grad_nd(self.perm[BB + 1], xf-1.0, yf-1.0, zf-1.0)

        x00 = lerp(n000, n100, u); x01 = lerp(n001, n101, u)
        x10 = lerp(n010, n110, u); x11 = lerp(n011, n111, u)
        y0  = lerp(x00, x10, v);   y1  = lerp(x01, x11, v)
        return lerp(y0, y1, w)
