from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from ..core_types import FBMParams
from ..registry import get_noise

@dataclass
class TwoDParams:
    width: int = 256
    height: int = 256
    scale: float = 128.0
    seed: int = 1337
    backend: str = "perlin2d"  # perlin2d | worley2d | diamond_square2d
    fbm: FBMParams = FBMParams()
    worley_cells: int = 32
    worley_metric: str = "euclid"
    ds_size: int = 257
    ds_roughness: float = 0.5

def generate_2d(params: TwoDParams) -> np.ndarray:
    if params.backend == "diamond_square2d":
        ds = get_noise("diamond_square2d", params.seed, params.ds_size, params.ds_roughness)
        return ds.sample()

    yy, xx = np.mgrid[0:params.height, 0:params.width]
    x = (xx.astype(np.float32) / params.scale)
    y = (yy.astype(np.float32) / params.scale)

    if params.backend == "worley2d":
        noise = get_noise("worley2d", params.seed, params.worley_cells, params.worley_metric)
        return noise.sample(x / (params.width/params.scale), y / (params.height/params.scale))

    noise = get_noise(params.backend, params.seed)
    out = np.zeros((params.height, params.width), dtype=np.float32)
    amp = 1.0; freq = 1.0; total = 0.0
    for _ in range(params.fbm.octaves):
        out += amp * noise.sample(x * freq, y * freq)
        total += amp
        amp *= params.fbm.gain; freq *= params.fbm.lacunarity
    out /= max(total, 1e-9)
    out = (out - out.min()) / (out.max() - out.min() + 1e-9)
    return out
