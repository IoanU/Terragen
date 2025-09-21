import numpy as np
from PIL import Image

def save_npy(h: np.ndarray, path: str):
    np.save(path, h.astype(np.float32))

def save_png(h: np.ndarray, path: str):
    img = (h*255.0).clip(0,255).astype(np.uint8)
    Image.fromarray(img, mode="L").save(path)

def save_obj(h: np.ndarray, path: str, z_scale: float = 50.0):
    H,W = h.shape
    with open(path, "w") as f:
        # vertices
        for y in range(H):
            for x in range(W):
                z = float(h[y,x])*z_scale
                f.write(f"v {x} {z} {y}\n")
        # faces (two triangles per cell)
        def vid(x,y): return y*W + x + 1
        for y in range(H-1):
            for x in range(W-1):
                v1=vid(x,y); v2=vid(x+1,y); v3=vid(x,y+1); v4=vid(x+1,y+1)
                f.write(f"f {v1} {v2} {v3}\n")
                f.write(f"f {v2} {v4} {v3}\n")
