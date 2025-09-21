#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "fbm.h"
#include "diamond_square.h"
#include "erosion.h"

namespace py = pybind11;

PYBIND11_MODULE(terragen_core, m) {
  m.def("fbm2d", &fbm2d, "FBM-Perlin 2D",
        py::arg("width"), py::arg("height"), py::arg("seed"),
        py::arg("octaves")=6, py::arg("lacunarity")=2.0, py::arg("gain")=0.5, py::arg("scale")=8.0);
  m.def("diamond_square", &diamond_square, "Diamond–Square 2D",
        py::arg("n_power"), py::arg("seed"), py::arg("roughness")=0.8f);
  m.def("thermal_erosion", &thermal_erosion, "Thermal erosion in-place",
        py::arg("heightmap"), py::arg("W"), py::arg("H"), py::arg("iters")=50, py::arg("talus")=0.012f);
}
