# Modular Terrain Generator

A modular Python package for **1D and 2D terrain generation** (side-scroller profiles or 2D heightmaps for games). Supports multiple procedural noise methods (Perlin, Worley, Diamond–Square) and post-processing with **erosion algorithms (thermal and hydraulic)** for realistic results.

The project is designed to be **plugin-friendly**, so it can easily be integrated into 2D or 3D games (as a heightmap/mesh generator).

---

## 📦 Dependencies
- Python **3.10+**
- **numpy** – numeric computing & arrays
- **matplotlib** – visualization and PNG export

Install:
```bash
pip install -r requirements.txt
```
`requirements.txt`:
```text
numpy
matplotlib
```

---

## ⚙️ CLI Arguments

Example run:
```bash
python -m terragen.cli --dim 2 --width 512 --height 512 --backend perlin2d --octaves 6 --show
```

### General
- `--dim {1,2}` – dimension: 1D (terrain profile) or 2D (heightmap).
- `--seed` – RNG seed (deterministic results).
- `--backend` – noise backend (`perlin1d`, `perlin2d`, `worley2d`, `diamond_square2d`).
- `--list-noise` – list all available noise backends.
- `--show` – open visualization with Matplotlib.
- `--export-png` – export result as PNG image (saved into `results/pictures/`).
- `--export-obj` – export heightmap as `.obj` mesh (saved into `results/values/`).
- `--vertical-scale` – vertical scale factor for `.obj` meshes.

### fBm Parameters
- `--octaves` – number of octaves (layers of noise).
- `--lacunarity` – frequency multiplier between octaves.
- `--gain` – amplitude reduction factor between octaves.

### 1D
- `--length` – length of the profile.
- `--scale1d` – X scale factor for noise input.

### 2D
- `--width`, `--height` – map size.
- `--scale2d` – XY scale factor for noise input.
- `--worley-cells` – number of cells for Worley noise.
- `--worley-metric` – distance metric (`euclid`, `manhattan`, `chebyshev`).
- `--ds-size` – size for Diamond–Square (power of 2 + 1).
- `--ds-roughness` – roughness coefficient for Diamond–Square.

### Erosion (post-process)
- `--erosion {none, thermal, hydraulic}` – type of erosion.

**Thermal:**
- `--erosion-iters` – number of iterations.
- `--talus` – slope threshold to trigger erosion.
- `--erode-factor` – how much material moves each step.

**Hydraulic:**
- `--rain-drops` – number of simulated raindrops (20k default for 2D, ~8k for 1D).
- `--inertia` – inertia of water droplets.
- `--capacity` – sediment carrying capacity.
- `--min-slope` – minimum slope.
- `--erode` – erosion rate.
- `--deposit` – deposition rate.
- `--evap` – evaporation rate.

---

## 📁 Project Structure

```
terragen/
├── __init__.py
├── cli.py              # CLI entry point
├── rng.py              # RNG utilities
├── core_types.py            # types and FBMParams
├── registry.py         # backend registry
├── pipelines/          # generation pipelines
│   ├── one_d.py        # 1D profile generation
│   └── two_d.py        # 2D map generation
├── noise/              # noise algorithms
│   ├── base.py
│   ├── perlin.py
│   ├── worley.py
│   └── diamond_square.py
├── post/               # post-processing
│   └── erosion.py      # thermal & hydraulic erosion
├── viz/                # visualization
│   └── matplotlib_viz.py
└── export/             # exporters
    ├── png.py
    └── obj.py

results/
├── pictures/           # PNG outputs
└── values/             # OBJ and other numeric outputs
```

---

## 🗂️ Output Directories
All examples below can save results into two folders:
- `results/pictures/` – exported images (PNG) and quick previews
- `results/values/` – raw numeric outputs (e.g., `.npy`) and meshes (e.g., `.obj`)

Create them once:
```bash
mkdir -p results/pictures results/values
```

> Note: The CLI exports PNG and OBJ via `--export-png` and `--export-obj`. To save raw arrays (`.npy`), load the library in Python and use `numpy.save('results/values/file.npy', data)`.

---

## ▶️ Usage Examples

### 1D + visualization:
```bash
python -m terragen.cli --dim 1 --length 1024 --scale1d 90 --seed 42 \
  --octaves 6 --erosion thermal --erosion-iters 80 --talus 0.012 --erode-factor 0.55 --export-png results/pictures/line.png --show
```

### 2D + export PNG:
```bash
python -m terragen.cli --dim 2 --width 512 --height 512 --scale2d 160 --seed 7 \
  --backend perlin2d --octaves 6 --lacunarity 2.0 --gain 0.5 \
  --erosion hydraulic --rain-drops 30000 \
  --export-png results/pictures/map.png --show
```

### 2D Worley “islands”:
```bash
python -m terragen.cli --dim 2 --backend worley2d --width 512 --height 512 \
  --worley-cells 40 --worley-metric euclid \
  --erosion thermal --erosion-iters 60 \
  --export-png results/pictures/worley.png --show
```

Results will be visualized with Matplotlib (`--show`) and automatically stored in the `results/` directory.

---

### Examples that save into `results/`

**1D + thermal + PNG to `results/pictures/`:**
```bash
python -m terragen.cli --dim 1 --length 1024 --scale1d 90 --seed 42 \
  --octaves 6 --erosion thermal --erosion-iters 80 --talus 0.012 --erode-factor 0.55 \
  --export-png results/pictures/line_1d_thermal.png --show
```

**2D Perlin + hydraulic + PNG to `results/pictures/`:**
```bash
python -m terragen.cli --dim 2 --width 512 --height 512 --scale2d 160 --seed 7 \
  --backend perlin2d --octaves 6 --lacunarity 2.0 --gain 0.5 \
  --erosion hydraulic --rain-drops 30000 \
  --export-png results/pictures/perlin2d_hydro.png --show
```

**2D Worley + thermal + PNG to `results/pictures/`:**
```bash
python -m terragen.cli --dim 2 --backend worley2d --width 512 --height 512 \
  --worley-cells 40 --worley-metric euclid \
  --erosion thermal --erosion-iters 60 \
  --export-png results/pictures/worley_thermal.png --show
```

**Export mesh OBJ to `results/values/`:**
```bash
python -m terragen.cli --dim 2 --width 257 --height 257 --backend perlin2d \
  --export-obj results/values/terrain.obj
```

**Save raw array (`.npy`) to `results/values/` (Python API):**
```python
import numpy as np
from terragen.pipelines.two_d import TwoDParams, generate_2d
p = TwoDParams(width=512, height=512, scale=160, seed=7)
hmap = generate_2d(p)
np.save('results/values/heightmap.npy', hmap)
```

---

## 🕹️ Use Cases
- procedural terrain for 2D side-scroller games
- heightmaps for 3D games (extruded in Unity/Unreal)
- stylized landscapes with erosion effects

---

## 📦 Dependencies

This project requires:
```
numpy
matplotlib
```

These can be installed with:
```bash
pip install -r requirements.txt
```

Or directly:
```bash
pip install numpy matplotlib
```
