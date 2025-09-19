from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from ..core_types import FBMParams
from ..registry import get_noise

@dataclass
class OneDParams:
    length: int = 512
    scale: float = 80.0
    seed: int = 1337
    backend: str = "perlin1d"
    fbm: FBMParams = FBMParams()

def generate_1d(params: OneDParams) -> np.ndarray:
    x = np.arange(params.length, dtype=np.float32) / params.scale
    noise = get_noise(params.backend, params.seed)
    out = np.zeros_like(x)
    amp = 1.0; freq = 1.0; total = 0.0
    for _ in range(params.fbm.octaves):
        out += amp * noise.sample(x * freq)
        total += amp
        amp *= params.fbm.gain; freq *= params.fbm.lacunarity
    out /= max(total, 1e-9)
    out = (out - out.min()) / (out.max() - out.min() + 1e-9)
    return out
