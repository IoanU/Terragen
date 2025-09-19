from __future__ import annotations
import random
import numpy as np
from .core_types import Seed

def make_rng(seed: Seed) -> np.random.Generator:
    random.seed(seed)
    return np.random.default_rng(seed)
