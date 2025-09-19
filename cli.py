from __future__ import annotations
import argparse
from .pipelines.one_d import OneDParams, generate_1d
from .pipelines.two_d import TwoDParams, generate_2d
from .viz import matplotlib_viz as viz
from .export.png import save_png
from .export.obj import save_obj
from .registry import list_noises
from .post.erosion import (
    thermal_erosion_2d, hydraulic_erosion_2d,
    thermal_erosion_1d, hydraulic_erosion_1d,
)

def build_parser():
    ap = argparse.ArgumentParser(description="Modular Terrain Generator")
    ap.add_argument("--dim", type=int, default=2, choices=[1,2])
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--backend", type=str, default=None, help="Noise backend (see --list-noise)")
    ap.add_argument("--list-noise", action="store_true", help="List available noise backends")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--export-png", type=str, default=None)
    ap.add_argument("--export-obj", type=str, default=None)
    ap.add_argument("--vertical-scale", type=float, default=60.0)

    # fBm
    ap.add_argument("--octaves", type=int, default=5)
    ap.add_argument("--lacunarity", type=float, default=2.0)
    ap.add_argument("--gain", type=float, default=0.5)

    # 1D
    ap.add_argument("--length", type=int, default=512)
    ap.add_argument("--scale1d", type=float, default=80.0)

    # 2D
    ap.add_argument("--width", type=int, default=256)
    ap.add_argument("--height", type=int, default=256)
    ap.add_argument("--scale2d", type=float, default=128.0)
    ap.add_argument("--worley-cells", type=int, default=32)
    ap.add_argument("--worley-metric", type=str, default="euclid")
    ap.add_argument("--ds-size", type=int, default=257)
    ap.add_argument("--ds-roughness", type=float, default=0.5)

    # Erosion
    ap.add_argument("--erosion", type=str, default="none", choices=["none","thermal","hydraulic"])
    ap.add_argument("--erosion-iters", type=int, default=50)      # thermal
    ap.add_argument("--talus", type=float, default=0.01)          # thermal
    ap.add_argument("--erode-factor", type=float, default=0.5)    # thermal

    ap.add_argument("--rain-drops", type=int, default=20000)      # hydraulic (2D); 1D folosește ~rain_drops//2
    ap.add_argument("--inertia", type=float, default=0.05)
    ap.add_argument("--capacity", type=float, default=4.0)
    ap.add_argument("--min-slope", type=float, default=0.01)
    ap.add_argument("--erode", type=float, default=0.3)
    ap.add_argument("--deposit", type=float, default=0.3)
    ap.add_argument("--evap", type=float, default=0.01)

    return ap

def __fbm(args):
    from .types import FBMParams
    return FBMParams(octaves=args.octaves, lacunarity=args.lacunarity, gain=args.gain)

def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)

    if args.list_noise:
        print("Available noise:", ", ".join(list_noises()))
        return

    if args.dim == 1:
        p = OneDParams(length=args.length, scale=args.scale1d, seed=args.seed,
                       backend=args.backend or "perlin1d", fbm=__fbm(args))
        line = generate_1d(p)

        if args.erosion == "thermal":
            line = thermal_erosion_1d(line, iterations=args.erosion_iters, talus=args.talus, factor=args.erode_factor)
        elif args.erosion == "hydraulic":
            line = hydraulic_erosion_1d(line, drops=max(1000, args.rain_drops//2), seed=args.seed,
                                        inertia=args.inertia, capacity=args.capacity, min_slope=args.min_slope,
                                        erosion=args.erode, deposition=args.deposit, evaporation=args.evap)

        if args.export_png:
            import numpy as np
            save_png(line[np.newaxis, :], args.export_png)
        if args.show:
            viz.show_1d(line)

    else:  # 2D
        backend = args.backend or "perlin2d"
        p = TwoDParams(width=args.width, height=args.height, scale=args.scale2d,
                       seed=args.seed, backend=backend, fbm=__fbm(args),
                       worley_cells=args.worley_cells, worley_metric=args.worley_metric,
                       ds_size=args.ds_size, ds_roughness=args.ds_roughness)
        hmap = generate_2d(p)

        if args.erosion == "thermal":
            hmap = thermal_erosion_2d(hmap, iterations=args.erosion_iters, talus=args.talus, factor=args.erode_factor)
        elif args.erosion == "hydraulic":
            hmap = hydraulic_erosion_2d(hmap, drops=args.rain_drops, seed=args.seed,
                                        inertia=args.inertia, capacity=args.capacity, min_slope=args.min_slope,
                                        erosion=args.erode, deposition=args.deposit, evaporation=args.evap)

        if args.export_png: save_png(hmap, args.export_png)
        if args.export_obj: save_obj(hmap, args.export_obj, args.vertical_scale)
        if args.show:
            viz.show_2d(hmap)

if __name__ == "__main__":
    main()
