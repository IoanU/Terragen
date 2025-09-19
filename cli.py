from __future__ import annotations
import argparse, os, datetime
import numpy as np
import terragen.noise
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

PICT_DIR = "terragen/results/pictures"
VAL_DIR = "terragen/results/values"

def ensure_dirs():
    os.makedirs(PICT_DIR, exist_ok=True)
    os.makedirs(VAL_DIR, exist_ok=True)

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def norm_out_path(path: str | None, kind: str, default_name: str, ext: str) -> str:
    """
    kind: 'png' -> PICT_DIR, 'obj'/'npy' -> VAL_DIR
    If path is None -> auto filename. If path has no directory -> put in the right folder.
    """
    base_dir = PICT_DIR if kind == "png" else VAL_DIR
    if not path or path.strip() == "":
        return os.path.join(base_dir, f"{default_name}.{ext}")
    # if user gave just a filename (no directory), place it in proper dir
    if os.path.dirname(path) == "":
        return os.path.join(base_dir, path)
    return path

def build_parser():
    ap = argparse.ArgumentParser(description="Modular Terrain Generator (1D/2D)")
    ap.add_argument("--dim", type=int, default=2, choices=[1,2])
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--backend", type=str, default=None, help="Noise backend (see --list-noise)")
    ap.add_argument("--list-noise", action="store_true", help="List available noise backends")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--export-png", type=str, default=None, help="PNG output path (filename or full path)")
    ap.add_argument("--export-obj", type=str, default=None, help="OBJ output path (filename or full path) (2D only)")
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

    ap.add_argument("--rain-drops", type=int, default=20000)      # hydraulic (2D); 1D uses ~rain_drops//2
    ap.add_argument("--inertia", type=float, default=0.05)
    ap.add_argument("--capacity", type=float, default=4.0)
    ap.add_argument("--min-slope", type=float, default=0.01)
    ap.add_argument("--erode", type=float, default=0.3)
    ap.add_argument("--deposit", type=float, default=0.3)
    ap.add_argument("--evap", type=float, default=0.01)

    # Saving behavior
    ap.add_argument("--no-save-npy", action="store_true",
                    help="Do not auto-save the generated array as .npy into results/values/")
    return ap

def __fbm(args):
    from .core_types import FBMParams
    return FBMParams(octaves=args.octaves, lacunarity=args.lacunarity, gain=args.gain)

def main(argv=None):
    ensure_dirs()
    ap = build_parser()
    args = ap.parse_args(argv)

    if args.list_noise:
        print("Available noise:", ", ".join(list_noises()))
        return

    erosion_tag = "none"
    if args.erosion == "thermal":
        erosion_tag = f"thermal{args.erosion_iters}"
    elif args.erosion == "hydraulic":
        erosion_tag = f"hydro{args.rain_drops}"

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

        # Auto-save NPY unless disabled
        if not args.no_save_npy:
            auto_name = f"line_{p.backend}_{erosion_tag}_{timestamp()}"
            npy_path = norm_out_path(None, "npy", auto_name, "npy")
            np.save(npy_path, line)
            print(f"[ok] Saved raw 1D array -> {npy_path}")

        # Export PNG if requested
        if True:  # normalize even if user gave just a filename
            default_name = f"line_{p.backend}_{erosion_tag}_{timestamp()}"
            if args.export_png is not None and args.export_png.strip() == "":
                # empty string means 'auto'
                png_path = norm_out_path(None, "png", default_name, "png")
                save_png(line[np.newaxis, :], png_path)
                print(f"[ok] Saved PNG -> {png_path}")
            elif args.export_png:
                png_path = norm_out_path(args.export_png, "png", default_name, "png")
                save_png(line[np.newaxis, :], png_path)
                print(f"[ok] Saved PNG -> {png_path}")

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

        # Auto-save NPY unless disabled
        if not args.no_save_npy:
            auto_name = f"map_{backend}_{erosion_tag}_{timestamp()}"
            npy_path = norm_out_path(None, "npy", auto_name, "npy")
            np.save(npy_path, hmap)
            print(f"[ok] Saved raw 2D array -> {npy_path}")

        # Normalize and save PNG if requested
        default_name = f"map_{backend}_{erosion_tag}_{timestamp()}"
        if args.export_png is not None and args.export_png.strip() == "":
            png_path = norm_out_path(None, "png", default_name, "png")
            save_png(hmap, png_path)
            print(f"[ok] Saved PNG -> {png_path}")
        elif args.export_png:
            png_path = norm_out_path(args.export_png, "png", default_name, "png")
            save_png(hmap, png_path)
            print(f"[ok] Saved PNG -> {png_path}")

        # Normalize and save OBJ if requested
        if args.export_obj is not None and args.export_obj.strip() == "":
            obj_path = norm_out_path(None, "obj", default_name, "obj")
            save_obj(hmap, obj_path, args.vertical_scale)
            print(f"[ok] Saved OBJ -> {obj_path}")
        elif args.export_obj:
            obj_path = norm_out_path(args.export_obj, "obj", default_name, "obj")
            save_obj(hmap, obj_path, args.vertical_scale)
            print(f"[ok] Saved OBJ -> {obj_path}")

        if args.show:
            viz.show_2d(hmap)

if __name__ == "__main__":
    main()
