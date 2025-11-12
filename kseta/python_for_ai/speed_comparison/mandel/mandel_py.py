#!/usr/bin/env python3
# mandel_py.py
"""
Backends:
  - scalar:     straightforward loops
  - numpy:      vectorized with broadcasting

Usage examples:
  # Render a PNG (640x480) and provide performance information
  python mandel_py.py --backend numpy --width 640 --height 480 --out mandel.png --bench

  # Benchmark only (no image)
  python mandel_py.py --backend scalar --bench
"""

from __future__ import annotations
import argparse
import time
from dataclasses import dataclass
from typing import Tuple, Optional

import numpy as np
from PIL import Image

try:
    from numba import njit, prange
    _HAVE_NUMBA = True
except Exception:
    _HAVE_NUMBA = False


@dataclass
class Viewport:
    x_min: float = -2.0
    x_max: float = +1.0
    y_min: float = -1.2
    y_max: float = +1.2
    max_iter: int = 100


def _palette(values: np.ndarray, max_iter: int) -> np.ndarray:
    """
    Map iteration counts to grayscale.
    Convention (matching the exercise notes): -1 means *did not escape*.
    We'll map -1 to 0 (black), others to a ramp [20..255] for visibility.
    """
    out = np.empty(values.shape, dtype=np.uint8)
    mask_in = values < 0  # inside set
    out[mask_in] = 0
    # scale iterations (1..max_iter) to a visible gradient (20..255)
    scale = 235.0 / max(1, max_iter)
    ramp = (values.astype(np.float32) * scale + 20.0).clip(0, 255).astype(np.uint8)
    out[~mask_in] = ramp[~mask_in]
    return out


# --- Scalar reference backend ---
def mandel_scalar(width: int, height: int, vp: Viewport) -> np.ndarray:
    """
    Return a (H, W) array with escape iteration or -1 if not escaped by max_iter.
    This is expectedly the performance relevant part!
    """
    xs = np.linspace(vp.x_min, vp.x_max, num=width, dtype=np.float64)
    ys = np.linspace(vp.y_min, vp.y_max, num=height, dtype=np.float64)
    img = np.empty((height, width), dtype=np.int32)

    for j in range(height):
        cy = ys[j]
        for i in range(width):
            cx = xs[i]
            x = 0.0
            y = 0.0
            it = 0
            while (x*x + y*y) <= 4.0 and it < vp.max_iter:
                # z = z^2 + c
                xt = x*x - y*y + cx
                y = 2.0*x*y + cy
                x = xt
                it += 1
            img[j, i] = -1 if it == vp.max_iter else it
    return img


# --- NumPy vectorized backend ---
def mandel_numpy(width: int, height: int, vp: Viewport) -> np.ndarray:
    xs = np.linspace(vp.x_min, vp.x_max, num=width, dtype=np.float64)
    ys = np.linspace(vp.y_min, vp.y_max, num=height, dtype=np.float64)
    X, Y = np.meshgrid(xs, ys)  # shape (H, W)

    # z starts at 0, c is fixed per pixel
    zr = np.zeros_like(X)  # real
    zi = np.zeros_like(Y)  # imag
    cr = X
    ci = Y

    escaped = np.zeros(X.shape, dtype=bool)
    esc_iter = np.full(X.shape, -1, dtype=np.int32)

    for it in range(1, vp.max_iter + 1):
        active = ~escaped
        if not np.any(active):
            break

        # Only on active pixels
        zr_a = zr[active]
        zi_a = zi[active]
        cr_a = cr[active]
        ci_a = ci[active]

        zr2 = zr_a * zr_a
        zi2 = zi_a * zi_a
        two_zr_zi = 2.0 * zr_a * zi_a

        zr_new = zr2 - zi2 + cr_a
        zi_new = two_zr_zi + ci_a

        mag2 = zr_new * zr_new + zi_new * zi_new
        just_escaped = mag2 > 4.0

        # Write back new z for still-active points
        zr_a[:] = zr_new
        zi_a[:] = zi_new
        zr[active] = zr_a
        zi[active] = zi_a

        # Record escape iteration and update mask
        esc_iter_active = esc_iter[active]
        esc_iter_active[just_escaped] = it
        esc_iter[active] = esc_iter_active
        escaped_active = escaped[active]
        escaped_active |= just_escaped
        escaped[active] = escaped_active

    return esc_iter


# --- Driver & utilities ---
def render(img_iters: np.ndarray, vp: Viewport, out_path: Optional[str]) -> None:
    if out_path is None:
        return
    img = _palette(img_iters, vp.max_iter)
    Image.fromarray(img, mode="L").save(out_path)


def compute(backend: str, width: int, height: int, vp: Viewport) -> np.ndarray:
    if backend == "scalar":
        return mandel_scalar(width, height, vp)
    if backend == "numpy":
        return mandel_numpy(width, height, vp)
    if backend == "numba":
        return mandel_numba(width, height, vp)
    raise ValueError(f"Unknown backend: {backend}")


# --- Main() ----
def main():
    p = argparse.ArgumentParser(description="Mandelbrot vectorization exercise – Python backends")
    p.add_argument("--backend", choices=["scalar", "numpy"], default="scalar")
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--height", type=int, default=480)
    p.add_argument("--max-iter", type=int, default=100)
    p.add_argument("--x", type=float, nargs=2, metavar=("XMIN", "XMAX"), default=(-2.0, 1.0))
    p.add_argument("--y", type=float, nargs=2, metavar=("YMIN", "YMAX"), default=(-1.2, 1.2))
    p.add_argument("--out", type=str, default=None, help="Output PNG path (omit to skip saving)")
    p.add_argument("--bench", action="store_true", help="Print timing")
    args = p.parse_args()

    vp = Viewport(x_min=args.x[0], x_max=args.x[1], y_min=args.y[0], y_max=args.y[1], max_iter=args.max_iter)

    t0 = time.perf_counter()
    iters = compute(args.backend, args.width, args.height, vp)
    t1 = time.perf_counter()

    if args.bench:
        print(f"Backend={args.backend:6s}  size={args.width}x{args.height}  "
              f"max_iter={args.max_iter:3d}  time={t1 - t0:.3f}s")

    render(iters, vp, args.out)


if __name__ == "__main__":
    main()
