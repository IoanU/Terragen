from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from ..rng import make_rng

@dataclass
class PermTable:
    seed: int
    p: np.ndarray

    @staticmethod
    def build(seed: int) -> "PermTable":
        rng = make_rng(seed)
        p = np.arange(256, dtype=np.int32)
        rng.shuffle(p)
        p = np.concatenate([p, p]).astype(np.int32)
        return PermTable(seed, p)

def fade(t):  # 6t^5 - 15t^4 + 10t^3
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)
