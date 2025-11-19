#!/usr/bin/env python3
# (c) Ihor Muraviov (Electronica)

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import mif
# =========================
# Config
# =========================
DAC_BITS   = 9       # DAC resolution (bits)
THRESHOLD  = 128      # black-pixel threshold (<= is black)
MARGIN     = 32       # keep waveform away from rails
FLIP_Y     = True     # flip Y so image is upright in XY mode

def luma_load(in_png: str) -> tuple[np.ndarray, int, int]:
    """load file as png image but converted to 8-bit grayscale, return (array, width, height)"""
    img = Image.open(in_png).convert("L")
    w, h = img.size
    luma_arr = np.array(img, dtype=np.uint8)
    return luma_arr, w, h

def luma_display(luma_arr: np.ndarray, w, h) -> None:
    """display luma array"""
    img = Image.fromarray(luma_arr.reshape((h, w)), mode="L")
    plt.imshow(img, cmap="gray", vmin=0, vmax=255)
    plt.title("Luma")
    plt.show()

def write_mem_hex(path: str, values: list[int], hex_width: int) -> None:
    """THISISRIDICULOUS Write list of integers as uppercase hex LINE BY LINE"""
    with open(path, "w") as f:
        f.writelines(f"{v:0{hex_width}X}\n" for v in values)

def luma_to_monochrome(gray: np.ndarray, thr: int) -> np.ndarray:
    """get boolean mask array from array"""
    return (gray <= thr)



def sort_normalize_optimize(mono: np.ndarray, bits: int, flip_y: bool = True, margin: int = 32):
    """
    Returns ordered lists X, Y normalized to DAC
    """
    def normalize_val(v, src_min, src_max, dst_min, dst_max):
        if src_max == src_min:
            # div by zero except
            return (dst_min + dst_max) // 2
        return round(dst_min + (v - src_min) * (dst_max - dst_min) / (src_max - src_min))

    def remove_duplicates(xs, ys):
        if not xs:
            return xs, ys
        nx, ny = [xs[0]], [ys[0]]
        for i in range(1, len(xs)):
            if xs[i] != nx[-1] or ys[i] != ny[-1]:
                nx.append(xs[i]); ny.append(ys[i])
        return nx, ny

    def interpolation(x0, y0, x1, y1, max_steps=8):
        """Return intermediate rounded points between (x0,y0) and (x1,y1)"""
        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)
        steps = min(max_steps, max(1, int(dist // 8)))
        mid_x, mid_y = [], []
        for s in range(1, steps + 1):
            t = s / (steps + 1)
            mid_x.append(round(x0 + dx * t))
            mid_y.append(round(y0 + dy * t))
        return mid_x, mid_y

    h, w = mono.shape
    dac_max = (1 << bits) - 1
    dst_min = margin
    dst_max = dac_max - margin
    if dst_min >= dst_max:
        dst_min = 0
        dst_max = dac_max
    # list of paths = list of (xpix, ypix) with x in [0,w-1], y in [0,h-1]
    ordered_paths = []  
    # find connected components 
    visited = np.zeros_like(mono, dtype=bool)
    comps = []
    for r in range(h):
        for c in range(w):
            if mono[r, c] and not visited[r, c]:
                stack = [(r, c)]
                visited[r, c] = True
                comp = []
                while stack:
                    yr, xc = stack.pop()
                    comp.append((xc, yr))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = yr + dy, xc + dx
                        if 0 <= ny < h and 0 <= nx < w and mono[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))
                comps.append(comp)

    # nearest neighbor
    for comp in comps:
        pts = comp[:]
        cur = min(pts, key=lambda p: (p[0], p[1]))
        path = [cur]
        pts_set = set(pts)
        pts_set.remove(cur)
        while pts_set:
            # get min of squared Euclidean distances
            nxt = min(pts_set, key=lambda p: (p[0]-cur[0])**2 + (p[1]-cur[1])**2)
            path.append(nxt)
            pts_set.remove(nxt)
            cur = nxt
        ordered_paths.append(path)

    # normalize
    X_total, Y_total = [], []
    for path in ordered_paths:
        if not path:
            continue
        xs = []
        ys = []
        for xpix, ypix in path:
            if flip_y:
                yrow = (h - 1 - ypix)
            else:
                yrow = ypix
            x_dac = normalize_val(xpix, 0, max(1, w - 1), dst_min, dst_max)
            y_dac = normalize_val(yrow, 0, max(1, h - 1), dst_min, dst_max)
            xs.append(int(x_dac)); ys.append(int(y_dac))
        xs, ys = remove_duplicates(xs, ys)
        if X_total and xs:
            rx, ry = interpolation(X_total[-1], Y_total[-1], xs[0], ys[0])
            X_total.extend(rx); Y_total.extend(ry)
        X_total.extend(xs); Y_total.extend(ys)

    return X_total, Y_total

def monochrome_display(mono: np.ndarray, w, h) -> None:
    """display monochrome"""
    img = Image.fromarray((mono * 255).astype(np.uint8).reshape((h, w)), mode="L")
    plt.imshow(img, cmap="gray", vmin=0, vmax=255)
    plt.title("Monochrome")
    plt.show()


def monochrome_to_xy_samples(mono: np.ndarray, flip_y: bool) -> tuple[list[int], list[int]]:
    """
    for each black pixel, emit one (X,Y)
    """
    h, w = mono.shape
    X, Y = [], []
    for r in range(h):
        for c in range(w):
            if mono[r, c]:
                X.append(c)
                Y.append((h - 1 - r) if flip_y else r)
    return X, Y

def monochrome_to_xy_samples_normalized(mono: np.ndarray, bits: int, flip_y: bool = True):
    """
    for each black NORMALIZED pixel, emit one (X,Y)
    """
    h, w = mono.shape
    dac_max = (1 << bits) - 1
    X, Y = [], []

    for r in range(h):
        for c in range(w):
            if mono[r, c]:
                x = round((c / (w - 1)) * dac_max) if w > 1 else dac_max // 2
                ypix = (h - 1 - r) if flip_y else r
                y = round((ypix / (h - 1)) * dac_max) if h > 1 else dac_max // 2

                X.append(x)
                Y.append(y)

    return X, Y

def xy_samples_display(X: list[int], Y: list[int]) -> None:
    """display XY samples"""
    plt.plot(X, Y, "k.")
    plt.title("XY Samples")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.show()

def downsample_xy(X: list[int], Y: list[int], decim: int):
    X_ds = X[::decim]
    Y_ds = Y[::decim]
    return X_ds, Y_ds

def main():
    in_png = "image.png"
    prefix = "image"

    gray, w, h = luma_load(in_png)
    luma_display(gray, w, h)
    mono = luma_to_monochrome(gray, THRESHOLD)
    monochrome_display(mono, w, h)


    #X, Y = monochrome_to_xy_samples(mono, False)
    #X, Y = monochrome_to_xy_samples_normalized(mono, DAC_BITS, FLIP_Y)
    X, Y = sort_normalize_optimize(mono, DAC_BITS, FLIP_Y, MARGIN)
    xy_samples_display(X, Y)
    X_ds, Y_ds = downsample_xy(X, Y, 8)
    xy_samples_display(X_ds, Y_ds)
    hexw = (DAC_BITS + 3) // 4
    write_mem_hex(f"{prefix}x.mem", X_ds, hexw)
    write_mem_hex(f"{prefix}y.mem", Y_ds, hexw)

    print(f"Done. Samples: {len(X_ds)}")
    print(f"Wrote: {prefix}x.mem, {prefix}y.mem")

if __name__ == "__main__":
    main()
