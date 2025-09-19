from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Literal, runtime_checkable
import numpy as np

ArrayLike = np.ndarray
Dim = Literal[1, 2]
Seed = int

@runtime_checkable
class Noise1D(Protocol):
    def sample(self, x: ArrayLike) -> ArrayLike: ...

@runtime_checkable
class Noise2D(Protocol):
    def sample(self, x: ArrayLike, y: ArrayLike) -> ArrayLike: ...

@dataclass
class FBMParams:
    octaves: int = 5
    lacunarity: float = 2.0
    gain: float = 0.5
