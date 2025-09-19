from __future__ import annotations
from typing import Callable, Dict

_NOISES: Dict[str, Callable[..., object]] = {}

def register_noise(name: str):
    def deco(ctor: Callable[..., object]):
        key = name.lower()
        if key in _NOISES:
            raise ValueError(f"Noise '{name}' already registered")
        _NOISES[key] = ctor
        return ctor
    return deco

def get_noise(name: str, *args, **kwargs):
    ctor = _NOISES.get(name.lower())
    if not ctor:
        raise KeyError(f"Unknown noise '{name}'. Available: {', '.join(sorted(_NOISES))}")
    return ctor(*args, **kwargs)

def list_noises():
    return sorted(_NOISES.keys())
