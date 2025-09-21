import numpy as np
import terragen_core as tc

def generate_2d(backend: str, seed: int, width: int, height: int,
                octaves=6, lacunarity=2.0, gain=0.5, scale=8.0,
                ds_power=9, ds_rough=0.8,
                erosion=None):
    if backend == "fbm":
        h = np.array(tc.fbm2d(width, height, int(seed), int(octaves), float(lacunarity), float(gain), float(scale)),
                     dtype=np.float32).reshape(height, width)
    elif backend == "diamond":
        size = (1<<ds_power)+1
        if width!=size or height!=size:
            raise ValueError(f"diamond backend requires width=height=(1<<n)+1, got {width}x{height}")
        h = np.array(tc.diamond_square(int(ds_power), int(seed), float(ds_rough)),
                     dtype=np.float32).reshape(height, width)
    else:
        raise ValueError("backend must be 'fbm' or 'diamond'")

    if erosion is not None:
        if erosion == "thermal":
            buf = h.flatten().tolist()
            tc.thermal_erosion(buf, h.shape[1], h.shape[0], iters=50, talus=0.012)
            h = np.array(buf, dtype=np.float32).reshape(h.shape)
        # (hydraulic simplified could be added later)
    return np.clip(h, 0.0, 1.0)
