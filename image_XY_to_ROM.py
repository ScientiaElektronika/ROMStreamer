#!/usr/bin/env python3
# (c) Ihor Muraviov (Electronica)

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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
    X, Y = monochrome_to_xy_samples_normalized(mono, DAC_BITS, FLIP_Y)
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
