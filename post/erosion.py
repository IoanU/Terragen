from __future__ import annotations
import numpy as np
from ..rng import make_rng

__all__ = [
    "thermal_erosion", "hydraulic_erosion",
    "thermal_erosion_1d", "hydraulic_erosion_1d",
    "thermal_erosion_2d", "hydraulic_erosion_2d",
]

# ---------------- Thermal (2D & 1D) ----------------

def thermal_erosion_2d(hmap: np.ndarray, iterations: int = 50, talus: float = 0.01, factor: float = 0.5) -> np.ndarray:
    H, W = hmap.shape
    hm = hmap.copy().astype(np.float32)
    for _ in range(iterations):
        for y in range(1, H-1):
            for x in range(1, W-1):
                diffs = []
                for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ny, nx = y+dy, x+dx
                    d = hm[y,x] - hm[ny,nx]
                    if d > talus: diffs.append((ny,nx,d))
                if diffs:
                    total = sum(d for *_, d in diffs)
                    for ny, nx, d in diffs:
                        delta = factor * (d/total) * (hm[y,x]-hm[ny,nx])
                        hm[y,x] -= delta
                        hm[ny,nx] += delta
    hm -= hm.min(); den = hm.max() - 1e-9; hm /= den
    return hm

def thermal_erosion_1d(line: np.ndarray, iterations: int = 50, talus: float = 0.01, factor: float = 0.5) -> np.ndarray:
    arr = line.copy().astype(np.float32)
    n = len(arr)
    for _ in range(iterations):
        for i in range(1, n-1):
            diffs = []
            for j in (i-1, i+1):
                d = arr[i] - arr[j]
                if d > talus: diffs.append((j, d))
            if diffs:
                total = sum(d for _, d in diffs)
                for j, d in diffs:
                    delta = factor * (d/total) * (arr[i]-arr[j])
                    arr[i] -= delta; arr[j] += delta
    arr -= arr.min(); den = arr.max() - 1e-9; arr /= den
    return arr

# generic wrapper (for compatibility with your previous canvas)
def thermal_erosion(hmap: np.ndarray, **kwargs) -> np.ndarray:
    return thermal_erosion_2d(hmap, **kwargs)

# ---------------- Hydraulic (2D & 1D) ----------------

def hydraulic_erosion_2d(hmap: np.ndarray, drops: int = 20000, seed: int = 1337, inertia: float = 0.05,
                         capacity: float = 4.0, min_slope: float = 0.01, erosion: float = 0.3, deposition: float = 0.3,
                         evaporation: float = 0.01) -> np.ndarray:
    rng = make_rng(seed)
    H, W = hmap.shape
    hm = hmap.copy().astype(np.float32)

    def clamp(p):
        y, x = p
        y = int(np.clip(y, 1, H-2)); x = int(np.clip(x, 1, W-2))
        return y, x

    for _ in range(drops):
        y = float(rng.integers(1, H-1)); x = float(rng.integers(1, W-1))
        vy = vx = 0.0; w = 1.0; s = 0.0
        for _ in range(50):  # lifetime
            iy, ix = clamp((y, x))
            h = hm[iy, ix]
            gx = (hm[iy, ix+1] - hm[iy, ix-1]) * 0.5
            gy = (hm[iy+1, ix] - hm[iy-1, ix]) * 0.5
            vx = vx * inertia - gx * (1-inertia)
            vy = vy * inertia - gy * (1-inertia)
            vlen = (vx*vx + vy*vy)**0.5 + 1e-9
            vx /= vlen; vy /= vlen
            x += vx; y += vy
            ny, nx = clamp((y, x))
            dh = hm[ny, nx] - h
            cap = max(-dh, min_slope) * vlen * w * capacity
            if s > cap:  # deposit
                amt = min((s - cap) * deposition, s)
                hm[iy, ix] += amt; s -= amt
            else:       # erode
                amt = min((cap - s) * erosion, hm[iy, ix])
                hm[iy, ix] -= amt; s += amt
            w *= (1.0 - evaporation)
            if w < 0.01: break
    hm -= hm.min(); den = hm.max() - 1e-9; hm /= den
    return hm

def hydraulic_erosion_1d(line: np.ndarray, drops: int = 8000, seed: int = 1337, inertia: float = 0.05,
                         capacity: float = 4.0, min_slope: float = 0.01, erosion: float = 0.3, deposition: float = 0.3,
                         evaporation: float = 0.01) -> np.ndarray:
    rng = make_rng(seed)
    arr = line.copy().astype(np.float32)
    n = len(arr)
    for _ in range(drops):
        i = int(rng.integers(1, n-1))
        v = 0.0; w = 1.0; s = 0.0
        for _ in range(50):
            g = (arr[min(i+1, n-1)] - arr[max(i-1, 0)]) * 0.5
            v = v * inertia - g * (1-inertia)
            j = int(np.clip(i + (-1 if v < 0 else 1), 1, n-2))
            dh = arr[j] - arr[i]
            cap = max(-dh, min_slope) * abs(v) * w * capacity
            if s > cap:
                amt = min((s - cap) * deposition, s)
                arr[i] += amt; s -= amt
            else:
                amt = min((cap - s) * erosion, arr[i])
                arr[i] -= amt; s += amt
            w *= (1.0 - evaporation)
            i = j
            if w < 0.01: break
    arr -= arr.min(); den = arr.max() - 1e-9; arr /= den
    return arr

# generic wrapper (for compatibility with your previous canvas)
def hydraulic_erosion(hmap: np.ndarray, **kwargs) -> np.ndarray:
    return hydraulic_erosion_2d(hmap, **kwargs)
