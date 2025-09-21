import argparse, os
from .core import generate_2d
from .exports import save_npy, save_png, save_obj
from .visualize import show_heightmap

def main():
    p = argparse.ArgumentParser("terragen")
    p.add_argument("--backend", choices=["fbm","diamond"], required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--width", type=int, default=513)
    p.add_argument("--height", type=int, default=513)
    p.add_argument("--octaves", type=int, default=6)
    p.add_argument("--lacunarity", type=float, default=2.0)
    p.add_argument("--gain", type=float, default=0.5)
    p.add_argument("--scale", type=float, default=8.0)
    p.add_argument("--ds-power", type=int, default=9, help="diamond-square n so size=(1<<n)+1")
    p.add_argument("--ds-rough", type=float, default=0.8)
    p.add_argument("--erosion", choices=["thermal"], default=None)
    p.add_argument("--export-npy", type=str)
    p.add_argument("--export-png", type=str)
    p.add_argument("--export-obj", type=str)
    p.add_argument("--show", action="store_true")
    args = p.parse_args()

    h = generate_2d(
        backend=args.backend, seed=args.seed, width=args.width, height=args.height,
        octaves=args.octaves, lacunarity=args.lacunarity, gain=args.gain, scale=args.scale,
        ds_power=args.ds_power, ds_rough=args.ds_rough, erosion=args.erosion
    )

    if args.export_npy: save_npy(h, args.export_npy)
    if args.export_png: save_png(h, args.export_png)
    if args.export_obj: save_obj(h, args.export_obj)
    if args.show: show_heightmap(h)
