# Terragen 🌍

A modular terrain generator with a fast C++ noise core (via [pybind11](https://github.com/pybind/pybind11)) and a Python front-end for visualization & exports.  
Designed as a developer tool for voxel and open-world games (Minecraft-like, survival sandbox, etc.).

---

## 🚀 Features (MVP)
- **Noise backends**: Perlin (1D/2D), Diamond–Square (2D).
- **fBm (Fractal Brownian Motion)**: octaves, lacunarity, gain.
- **Post-processing**: thermal + hydraulic erosion (simplified).
- **Export options**:
  - `.npy` (NumPy array, fast reload)
  - `.png` (grayscale heightmap)
  - `.obj` (3D mesh)
- **Visualization**: quick preview with matplotlib.

---

## 📂 Project Structure
```
terragen/
├── CMakeLists.txt          # CMake build config
├── pyproject.toml          # Python build/install config
├── README.md               # This file
├── cpp/                    # C++ core noise + erosion
│   ├── bindings.cpp        # Pybind11 bindings
│   ├── perlin.cpp/.h       # Perlin noise implementation
│   ├── fbm.cpp/.h          # fBm wrapper (octaves, lacunarity, gain)
│   ├── diamond_square.cpp/.h # Diamond–Square algorithm
│   └── erosion.cpp/.h      # Thermal/hydraulic erosion
├── python/
│   └── terragen/
│       ├── __init__.py     # Package entry
│       ├── core.py         # High-level Python API (calls C++ core)
│       ├── cli.py          # CLI wrapper
│       ├── exports.py      # Exporter to PNG/OBJ/NPY
└       └── visualize.py    # Visual preview
```

---

## 📦 Requirements

### Build requirements
- **CMake ≥ 3.15**
- **C++17 compiler** (tested with MSVC and g++)
- **Python ≥ 3.9**
- **[pybind11](https://github.com/pybind/pybind11) ≥ 2.12**  
  (fetched automatically if not found)

### Python dependencies (auto-installed)
- `numpy`
- `pillow`
- `matplotlib`
- `setuptools>=61`
- `scikit-build-core>=0.11`
- `wheel`

---

## 🔧 Build & Install

### 1) Clone repo
```bash
git clone https://github.com/IoanU/terragen.git
cd terragen
```

### 2) Build C++ core
```bash
cmake -S . -B build -G "Ninja" -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

### 3) Install Python package
```bash
python -m pip install -v .
```

---

## 🖥️ Usage

### CLI
Run from terminal:
```bash
terragen --backend fbm --seed 1337 --dim 128 128 --octaves 6 --erosion thermal --export-png terrain.png --show
```

### Python API
```python
import terragen

h = terragen.generate_2d(
    backend="fbm",
    seed=1337,
    width=128,
    height=128,
    octaves=6,
    erosion="thermal"
)

print("Shape:", h.shape, "min:", float(h.min()), "max:", float(h.max()))
```

---

## ⚙️ CLI Arguments

| Argument           | Type      | Description |
|--------------------|-----------|-------------|
| `--backend`        | str       | Noise algorithm: `perlin`, `fbm`, `diamond_square`. |
| `--seed`           | int       | Seed for deterministic terrain generation. Same seed → same terrain. |
| `--dim`            | int int   | Dimensions of the generated map (width × height). |
| `--octaves`        | int       | Number of octaves (for fBm). More octaves = more detail. |
| `--lacunarity`     | float     | Frequency multiplier between octaves (default: 2.0). |
| `--gain`           | float     | Amplitude multiplier between octaves (default: 0.5). |
| `--erosion`        | str       | Apply erosion: `thermal`, `hydraulic`, or `none`. |
| `--export-npy`     | path      | Save result as NumPy `.npy` file. |
| `--export-png`     | path      | Save result as PNG grayscale heightmap. |
| `--export-obj`     | path      | Save result as 3D mesh (`.obj`). |
| `--show`           | flag      | Show result with matplotlib. |

---

## 📸 Example

**Input:**
```bash
terragen --backend diamond_square --seed 42 --dim 64 64 --export-png demo.png --show
```

**Output:**
- A `64×64` heightmap saved as `demo.png`.
- Matplotlib preview window.

---

## 🛠️ Roadmap
- [ ] Biome masks (desert, mountains, rivers)
