"""
Segmentasi Warna Merah pada Citra
Ahmad Hanif Abiyyu Khrisna
2125640006
STr-LJ Teknik Elektronika
Pengolahan Citra 

Framework: Python 3 + OpenCV 4 + NumPy (no deep learning)
"""
import cv2
import numpy as np
import os
import argparse

# === PARAMETER DEFAULT (HSV ranges) ===========================================
# Hue di OpenCV berskala 0-179 (bukan 0-359), karena disimpan dalam uint8.
# Warna merah "membungkus" titik 0, sehingga butuh DUA rentang terpisah.
LOWER_RED_1 = np.array([  0, 120,  70])  # Rentang merah-bawah  (0°  - 10°)
UPPER_RED_1 = np.array([ 10, 255, 255])
LOWER_RED_2 = np.array([170, 120,  70])  # Rentang merah-atas  (170° - 180°)
UPPER_RED_2 = np.array([180, 255, 255])

KERNEL = np.ones((5, 5), np.uint8)  # Structuring element untuk morfologi

def segment_red(img_bgr,
                low1=LOWER_RED_1, up1=UPPER_RED_1,
                low2=LOWER_RED_2, up2=UPPER_RED_2,
                use_morph=True):
    """Segmentasi piksel merah dari citra BGR -> (mask biner, citra hasil)."""
    # 1. Konversi ruang warna BGR -> HSV
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # 2. Threshold dua rentang Hue
    mask1 = cv2.inRange(hsv, low1, up1)
    mask2 = cv2.inRange(hsv, low2, up2)

    # 3. Gabungkan mask (OR logical) -> seluruh piksel merah jadi putih
    mask = cv2.bitwise_or(mask1, mask2)

    # 4. Bersihkan noise: OPEN hapus bintik kecil, CLOSE tutup lubang dlm objek
    if use_morph:
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  KERNEL, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

    # 5. Tampilkan hanya piksel merah dari citra asli
    result = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
    return mask, result


def adjust_brightness(img, factor):
    """Simulasi kondisi pencahayaan: factor>1 terang, factor<1 redup."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 2] = np.clip(hsv[..., 2] * factor, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def red_pixel_ratio(mask):
    return 100.0 * np.count_nonzero(mask) / mask.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input',  default='mobil.jpg')
    ap.add_argument('--outdir', default='output')
    ap.add_argument('--width',  type=int, default=800,
                    help='Resize width agar ringan di RPi (0 = no resize)')
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    img = cv2.imread(args.input)
    if img is None:
        raise FileNotFoundError(f"Tidak dapat membaca {args.input}")

    if args.width > 0 and img.shape[1] > args.width:
        scale = args.width / img.shape[1]
        img = cv2.resize(img, (args.width, int(img.shape[0] * scale)),
                         interpolation=cv2.INTER_AREA)

    # ---- EKSPERIMEN 1: Threshold default ------------------------------------
    mask, res = segment_red(img)
    cv2.imwrite(f'{args.outdir}/01_original.jpg', img)
    cv2.imwrite(f'{args.outdir}/02_mask_default.jpg', mask)
    cv2.imwrite(f'{args.outdir}/03_result_default.jpg', res)
    print(f"[Default ]  Red ratio = {red_pixel_ratio(mask):6.2f}%")

    # ---- EKSPERIMEN 2: Threshold "ketat" (saturation tinggi) ----------------
    mask_t, res_t = segment_red(
        img,
        low1=np.array([0,   200, 100]), up1=np.array([8,   255, 255]),
        low2=np.array([172, 200, 100]), up2=np.array([180, 255, 255]))
    cv2.imwrite(f'{args.outdir}/04_mask_tight.jpg',   mask_t)
    cv2.imwrite(f'{args.outdir}/05_result_tight.jpg', res_t)
    print(f"[Tight   ]  Red ratio = {red_pixel_ratio(mask_t):6.2f}%")

    # ---- EKSPERIMEN 3: Threshold "longgar" ----------------------------------
    mask_l, res_l = segment_red(
        img,
        low1=np.array([0,   60, 40]),  up1=np.array([15,  255, 255]),
        low2=np.array([160, 60, 40]),  up2=np.array([180, 255, 255]))
    cv2.imwrite(f'{args.outdir}/06_mask_loose.jpg',   mask_l)
    cv2.imwrite(f'{args.outdir}/07_result_loose.jpg', res_l)
    print(f"[Loose   ]  Red ratio = {red_pixel_ratio(mask_l):6.2f}%")

    # ---- EKSPERIMEN 4: Pencahayaan terang & redup ---------------------------
    bright = adjust_brightness(img, 1.6)
    dim    = adjust_brightness(img, 0.4)

    mb, rb = segment_red(bright)
    md, rd = segment_red(dim)
    cv2.imwrite(f'{args.outdir}/08_bright_input.jpg', bright)
    cv2.imwrite(f'{args.outdir}/09_bright_mask.jpg',  mb)
    cv2.imwrite(f'{args.outdir}/10_dim_input.jpg',    dim)
    cv2.imwrite(f'{args.outdir}/11_dim_mask.jpg',     md)
    print(f"[Bright  ]  Red ratio = {red_pixel_ratio(mb):6.2f}%")
    print(f"[Dim     ]  Red ratio = {red_pixel_ratio(md):6.2f}%")

    print(f"\n[OK] Semua hasil tersimpan di '{args.outdir}/'")


if __name__ == '__main__':
    main()