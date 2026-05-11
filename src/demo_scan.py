"""
Demo Scan Animation - Pipeline Visualization
Pengolahan Citra - PENS 2026

Membuat animasi pipeline pengolahan citra yang bisa direkam jadi video MP4
atau ditampilkan live untuk presentasi.

Output:
- MP4 video (untuk PPT)
- Sequence frames PNG
- Live window OpenCV (mode --live)

Penggunaan:
    python3 demo_scan.py --input mobil.jpg --outdir scan_demo
    python3 demo_scan.py --input mobil.jpg --live   # live mode
"""
import cv2
import numpy as np
import os
import argparse
import time
from pathlib import Path

# Import pipeline dari script utama
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segmentasi_merah_v2 import (
    LOWER_RED_1, UPPER_RED_1, LOWER_RED_2, UPPER_RED_2,
    KERNEL_OPEN, KERNEL_CLOSE,
    stage_hsv, stage_threshold, stage_combine,
    stage_morphology, stage_filter_contours, stage_draw_bbox,
)

# === KONFIGURASI ANIMASI =================================================
FPS = 30                  # frame rate output video
HOLD_FRAMES = 60          # tahan tiap stage 2 detik
SCAN_FRAMES = 45          # animasi scan-line 1.5 detik
TRANSITION_FRAMES = 15    # transisi 0.5 detik

# Warna UI (BGR)
COLOR_BG       = (28, 28, 35)      # dark background
COLOR_TITLE    = (255, 255, 255)
COLOR_ACCENT   = (39, 51, 153)     # cherry red BGR
COLOR_TEXT     = (220, 220, 220)
COLOR_HIGHLIGHT = (24, 197, 245)   # gold/yellow accent
COLOR_OK       = (0, 255, 0)


# === HELPER UI ===========================================================
def make_canvas(w, h):
    """Buat canvas dengan background gradient dark."""
    canvas = np.full((h, w, 3), COLOR_BG, dtype=np.uint8)
    return canvas


def overlay_text(canvas, text, pos, scale=0.7, color=COLOR_TEXT, thick=1, font=cv2.FONT_HERSHEY_SIMPLEX):
    cv2.putText(canvas, text, pos, font, scale, color, thick, cv2.LINE_AA)


def overlay_box(canvas, x, y, w, h, color, thick=2):
    cv2.rectangle(canvas, (x, y), (x + w, y + h), color, thick)


def fit_to_box(img, box_w, box_h):
    """Resize image to fit dalam box (preserve aspect ratio)."""
    h, w = img.shape[:2]
    scale = min(box_w / w, box_h / h)
    nw, nh = int(w * scale), int(h * scale)
    return cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA), nw, nh


def place_image(canvas, img, x, y, max_w, max_h):
    """Place image di canvas, center within max_w x max_h."""
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    fitted, nw, nh = fit_to_box(img, max_w, max_h)
    cx = x + (max_w - nw) // 2
    cy = y + (max_h - nh) // 2
    canvas[cy:cy + nh, cx:cx + nw] = fitted
    return cx, cy, nw, nh


def draw_progress_bar(canvas, x, y, w, h, progress, color=COLOR_HIGHLIGHT):
    """Progress bar 0.0 - 1.0."""
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (60, 60, 60), -1)
    fill_w = int(w * max(0, min(1, progress)))
    if fill_w > 0:
        cv2.rectangle(canvas, (x, y), (x + fill_w, y + h), color, -1)


# === FRAME BUILDERS PER STAGE ============================================
def render_header(canvas, stage_num, total_stages, stage_title, subtitle=""):
    """Header bar atas dengan info stage."""
    H, W = canvas.shape[:2]
    # Top bar
    cv2.rectangle(canvas, (0, 0), (W, 80), (40, 40, 50), -1)
    # Accent line
    cv2.rectangle(canvas, (0, 78), (W, 80), COLOR_ACCENT, -1)
    # Stage indicator
    overlay_text(canvas, f"STAGE {stage_num}/{total_stages}",
                 (30, 32), scale=0.6, color=COLOR_HIGHLIGHT, thick=2)
    overlay_text(canvas, stage_title,
                 (30, 65), scale=1.0, color=COLOR_TITLE, thick=2)
    if subtitle:
        overlay_text(canvas, subtitle,
                     (W - 600, 50), scale=0.55, color=COLOR_TEXT, thick=1)
    # Progress dots
    dot_w = 25
    start_x = W - 30 - (total_stages * (dot_w + 8))
    for i in range(total_stages):
        cx = start_x + i * (dot_w + 8) + dot_w // 2
        c = COLOR_HIGHLIGHT if i < stage_num else (80, 80, 90)
        cv2.circle(canvas, (cx, 30), 5, c, -1)


def render_footer(canvas, watermark="Pengolahan Citra | PENS 2026"):
    H, W = canvas.shape[:2]
    cv2.rectangle(canvas, (0, H - 35), (W, H), (30, 30, 38), -1)
    overlay_text(canvas, watermark,
                 (20, H - 12), scale=0.45, color=(150, 150, 160), thick=1)
    overlay_text(canvas, "Segmentasi Warna Merah - HSV Pipeline",
                 (W - 480, H - 12), scale=0.45, color=(150, 150, 160), thick=1)


def stage_intro_frames(canvas_size, title, subtitle, n_frames=HOLD_FRAMES):
    """Frame intro / title screen."""
    W, H = canvas_size
    frames = []
    for i in range(n_frames):
        canvas = make_canvas(W, H)
        # Big centered title
        text_size = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, 2.5, 4)[0]
        cv2.putText(canvas, title,
                    ((W - text_size[0]) // 2, H // 2 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, COLOR_TITLE, 4, cv2.LINE_AA)
        # Subtitle
        sub_size = cv2.getTextSize(subtitle, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
        cv2.putText(canvas, subtitle,
                    ((W - sub_size[0]) // 2, H // 2 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLOR_HIGHLIGHT, 2, cv2.LINE_AA)
        # Accent line (animated)
        progress = min(1.0, i / 30.0)
        line_w = int(300 * progress)
        cv2.rectangle(canvas,
                      ((W - line_w) // 2, H // 2 + 70),
                      ((W + line_w) // 2, H // 2 + 75),
                      COLOR_ACCENT, -1)
        frames.append(canvas)
    return frames


def stage_image_with_scan(canvas_size, img, stage_num, total, title, desc,
                          scan_frames=SCAN_FRAMES):
    """Frame menampilkan citra dengan animasi scan-line bergerak."""
    W, H = canvas_size
    frames = []
    box_w, box_h = W - 100, H - 250
    # Pre-compute placement
    test_canvas = make_canvas(W, H)
    cx, cy, nw, nh = place_image(test_canvas, img, 50, 130, box_w, box_h)

    for i in range(scan_frames):
        canvas = make_canvas(W, H)
        render_header(canvas, stage_num, total, title, desc)
        # Place image
        place_image(canvas, img, 50, 130, box_w, box_h)
        # Animated scan line
        progress = i / max(1, scan_frames - 1)
        scan_y = cy + int(nh * progress)
        # Glow effect — multiple lines
        for offset, alpha in [(-3, 0.3), (-2, 0.5), (-1, 0.7), (0, 1.0), (1, 0.7), (2, 0.5), (3, 0.3)]:
            if 0 < scan_y + offset < H:
                color = tuple(int(c * alpha) for c in COLOR_HIGHLIGHT)
                cv2.line(canvas, (cx, scan_y + offset), (cx + nw, scan_y + offset),
                         color, 1, cv2.LINE_AA)
        # Bright center line
        cv2.line(canvas, (cx, scan_y), (cx + nw, scan_y), (255, 255, 255), 1, cv2.LINE_AA)
        # Progress bar at bottom
        bar_y = H - 70
        overlay_text(canvas, f"Scanning {int(progress * 100)}%",
                     (50, bar_y - 8), scale=0.5, color=COLOR_HIGHLIGHT)
        draw_progress_bar(canvas, 50, bar_y, W - 100, 6, progress)
        render_footer(canvas)
        frames.append(canvas)
    return frames


def stage_hold_image(canvas_size, img, stage_num, total, title, desc,
                     n_frames=HOLD_FRAMES, annotation_lines=None):
    """Frame static menampilkan hasil tahap."""
    W, H = canvas_size
    frames = []
    box_w, box_h = W - 100, H - 250

    for i in range(n_frames):
        canvas = make_canvas(W, H)
        render_header(canvas, stage_num, total, title, desc)
        place_image(canvas, img, 50, 130, box_w, box_h)
        # Annotation list di bawah
        if annotation_lines:
            for j, line in enumerate(annotation_lines):
                overlay_text(canvas, line,
                             (50, H - 90 + j * 22),
                             scale=0.5, color=COLOR_TEXT)
        render_footer(canvas)
        frames.append(canvas)
    return frames


def stage_split_view(canvas_size, img_left, img_right, stage_num, total,
                     title, label_left, label_right, n_frames=HOLD_FRAMES,
                     stat_left=None, stat_right=None):
    """Side-by-side comparison frame."""
    W, H = canvas_size
    frames = []
    half_w = (W - 90) // 2
    box_h = H - 280

    for i in range(n_frames):
        canvas = make_canvas(W, H)
        render_header(canvas, stage_num, total, title, "")
        # Left
        place_image(canvas, img_left, 30, 130, half_w, box_h)
        cv2.putText(canvas, label_left, (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_HIGHLIGHT, 2, cv2.LINE_AA)
        if stat_left:
            cv2.putText(canvas, stat_left, (30, H - 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_OK, 2, cv2.LINE_AA)
        # Right
        right_x = 60 + half_w
        place_image(canvas, img_right, right_x, 130, half_w, box_h)
        cv2.putText(canvas, label_right, (right_x, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_HIGHLIGHT, 2, cv2.LINE_AA)
        if stat_right:
            cv2.putText(canvas, stat_right, (right_x, H - 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_OK, 2, cv2.LINE_AA)
        # Divider
        mid_x = W // 2
        cv2.line(canvas, (mid_x, 130), (mid_x, H - 60), (60, 60, 70), 2)
        render_footer(canvas)
        frames.append(canvas)
    return frames


def stage_outro_frames(canvas_size, n_objects, total_time_ms, fps_estimate,
                       n_frames=HOLD_FRAMES * 2):
    """Frame outro dengan stats final."""
    W, H = canvas_size
    frames = []
    for i in range(n_frames):
        canvas = make_canvas(W, H)
        # Big title
        title = "DETEKSI SELESAI"
        ts = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, 2.0, 4)[0]
        cv2.putText(canvas, title, ((W - ts[0]) // 2, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.0, COLOR_OK, 4, cv2.LINE_AA)

        # Stats grid (3 boxes)
        box_w = 280
        box_h = 200
        gap = 40
        total_w = box_w * 3 + gap * 2
        sx = (W - total_w) // 2
        sy = 240

        stats = [
            (f"{n_objects}", "Objek Terdeteksi", COLOR_ACCENT),
            (f"{total_time_ms:.1f} ms", "Waktu Eksekusi", (180, 180, 180)),
            (f"{fps_estimate:.0f} FPS", "Throughput Estimate", COLOR_HIGHLIGHT),
        ]

        for j, (val, lbl, c) in enumerate(stats):
            bx = sx + j * (box_w + gap)
            cv2.rectangle(canvas, (bx, sy), (bx + box_w, sy + box_h), (45, 45, 55), -1)
            cv2.rectangle(canvas, (bx, sy), (bx + box_w, sy + 6), c, -1)
            # Big value
            ts = cv2.getTextSize(val, cv2.FONT_HERSHEY_SIMPLEX, 1.6, 4)[0]
            cv2.putText(canvas, val,
                        (bx + (box_w - ts[0]) // 2, sy + 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, c, 4, cv2.LINE_AA)
            ts = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
            cv2.putText(canvas, lbl,
                        (bx + (box_w - ts[0]) // 2, sy + 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 1, cv2.LINE_AA)

        # Footer
        bottom = "Pipeline: BGR -> HSV -> Threshold -> Morphology -> Filter -> Detect"
        ts = cv2.getTextSize(bottom, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        cv2.putText(canvas, bottom,
                    ((W - ts[0]) // 2, H - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_HIGHLIGHT, 1, cv2.LINE_AA)
        frames.append(canvas)
    return frames


# === MAIN PIPELINE BUILDER ===============================================
def build_animation(img_path, canvas_size=(1280, 720)):
    """Build full animation untuk satu citra."""
    img = cv2.imread(str(img_path))
    if img is None:
        raise FileNotFoundError(img_path)

    # Resize for processing
    if img.shape[1] > 900:
        scale = 900 / img.shape[1]
        img = cv2.resize(img, (900, int(img.shape[0] * scale)),
                         interpolation=cv2.INTER_AREA)

    H, W = img.shape[:2]

    # Process all stages
    hsv = stage_hsv(img, use_clahe=False)
    m1, m2 = stage_threshold(hsv)
    mask_raw = stage_combine(m1, m2)
    mask_morph = stage_morphology(mask_raw)
    mask_filt, valid = stage_filter_contours(mask_morph, H * W)
    bbox_img = stage_draw_bbox(img, valid)
    result = cv2.bitwise_and(img, img, mask=mask_filt)

    TOTAL = 7
    all_frames = []

    # ----- Intro -----
    all_frames += stage_intro_frames(canvas_size,
        "SEGMENTASI WARNA MERAH",
        "HSV Pipeline | Pengolahan Citra | PENS")

    # ----- Stage 1: Input (with scan animation) -----
    all_frames += stage_image_with_scan(canvas_size, img, 1, TOTAL,
        "INPUT CITRA",
        "Citra BGR dibaca dengan cv2.imread()")
    all_frames += stage_hold_image(canvas_size, img, 1, TOTAL,
        "INPUT CITRA",
        f"Resolusi: {W} x {H} px",
        annotation_lines=[
            f"Format awal: BGR (Blue, Green, Red) - default OpenCV",
            f"Total piksel: {W*H:,}",
        ])

    # ----- Stage 2: HSV Conversion -----
    hsv_display = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    all_frames += stage_split_view(canvas_size, img, hsv_display, 2, TOTAL,
        "KONVERSI BGR -> HSV",
        "BGR (Original)", "HSV (Display approx)",
        stat_left="cv2.cvtColor(img, COLOR_BGR2HSV)",
        stat_right="Hue [0-179] | Sat [0-255] | Val [0-255]")

    # ----- Stage 3: Dual-range Threshold -----
    all_frames += stage_split_view(canvas_size, m1, m2, 3, TOTAL,
        "DUAL-RANGE THRESHOLDING",
        "Mask 1: Hue 0-10", "Mask 2: Hue 170-180",
        stat_left="cv2.inRange() rentang merah awal",
        stat_right="cv2.inRange() rentang merah akhir")

    # ----- Stage 4: Combine -----
    all_frames += stage_hold_image(canvas_size, mask_raw, 4, TOTAL,
        "GABUNG DUA MASK",
        "cv2.bitwise_or(mask1, mask2)",
        annotation_lines=[
            "Operasi OR per-bit menggabungkan kedua rentang Hue",
            f"Piksel teridentifikasi: {np.count_nonzero(mask_raw):,} ({100*np.count_nonzero(mask_raw)/mask_raw.size:.2f}%)",
        ])

    # ----- Stage 5: Morphology -----
    all_frames += stage_split_view(canvas_size, mask_raw, mask_morph, 5, TOTAL,
        "OPERASI MORFOLOGI",
        "Sebelum (raw)", "Setelah (OPEN + CLOSE)",
        stat_left=f"Bercak noise: {np.count_nonzero(mask_raw):,} px",
        stat_right=f"Setelah cleanup: {np.count_nonzero(mask_morph):,} px")

    # ----- Stage 6: Contour Filter -----
    all_frames += stage_split_view(canvas_size, mask_morph, mask_filt, 6, TOTAL,
        "FILTER KONTUR",
        "Sebelum filter", "Setelah filter (area+aspect)",
        stat_left=f"All contours detected",
        stat_right=f"Valid objects: {len(valid)}")

    # ----- Stage 7: Final Detection -----
    all_frames += stage_image_with_scan(canvas_size, bbox_img, 7, TOTAL,
        "DETEKSI FINAL",
        f"Bounding box pada {len(valid)} objek terdeteksi")
    all_frames += stage_hold_image(canvas_size, bbox_img, 7, TOTAL,
        "DETEKSI FINAL",
        f"{len(valid)} objek merah berhasil teridentifikasi",
        annotation_lines=[
            f"Bounding box hijau menunjukkan lokasi objek",
            f"Label: nomor objek + persentase area citra",
        ],
        n_frames=HOLD_FRAMES + 30)

    # ----- Outro -----
    # Hitung timing total dummy (dari 1 run cepat)
    t0 = time.time()
    _ = stage_hsv(img)
    _ = stage_threshold(_)
    elapsed = (time.time() - t0) * 1000
    all_frames += stage_outro_frames(canvas_size, len(valid),
                                     total_time_ms=elapsed * 4,  # estimasi total
                                     fps_estimate=1000 / (elapsed * 4) if elapsed > 0 else 100)

    return all_frames, valid


# === MAIN ================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input',  default='input/mobil.jpg')
    ap.add_argument('--outdir', default='scan_demo')
    ap.add_argument('--width',  type=int, default=1280, help='Canvas width')
    ap.add_argument('--height', type=int, default=720,  help='Canvas height')
    ap.add_argument('--live',   action='store_true', help='Tampilkan live window')
    ap.add_argument('--frames', action='store_true', help='Save individual PNG frames')
    ap.add_argument('--no-video', action='store_true', help='Skip MP4 generation')
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"  DEMO SCAN ANIMATION")
    print(f"  Input  : {args.input}")
    print(f"  Output : {outdir}/")
    print(f"  Canvas : {args.width}x{args.height} @ {FPS} fps")
    print(f"{'='*70}\n")

    print("[1/3] Building animation frames...")
    frames, valid = build_animation(args.input, (args.width, args.height))
    print(f"      Total frames: {len(frames)} ({len(frames)/FPS:.1f} detik)")
    print(f"      Objek terdeteksi: {len(valid)}\n")

    # ----- Save MP4 video -----
    if not args.no_video:
        print("[2/3] Encoding MP4 video...")
        video_path = outdir / 'demo_scan.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(video_path), fourcc, FPS,
                                 (args.width, args.height))
        for i, fr in enumerate(frames):
            writer.write(fr)
            if i % 30 == 0:
                print(f"      Frame {i}/{len(frames)}", end='\r')
        writer.release()
        print(f"      Saved: {video_path} ({video_path.stat().st_size//1024} KB)\n")

    # ----- Save individual frames -----
    if args.frames:
        print("[3/3] Saving individual frames...")
        frames_dir = outdir / 'frames'
        frames_dir.mkdir(exist_ok=True)
        # Save key frames only (1 per stage)
        key_indices = [0, 60, 180, 300, 420, 540, 660, 780, 900]
        key_indices = [i for i in key_indices if i < len(frames)]
        for idx in key_indices:
            cv2.imwrite(str(frames_dir / f'frame_{idx:04d}.png'), frames[idx])
        print(f"      Saved {len(key_indices)} key frames to {frames_dir}/\n")

    # ----- Live window mode -----
    if args.live:
        print("[Live] Tekan SPACE untuk play/pause, Q untuk keluar, R untuk replay")
        cv2.namedWindow('Demo Scan', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Demo Scan', args.width, args.height)
        idx = 0
        playing = True
        while True:
            cv2.imshow('Demo Scan', frames[idx])
            key = cv2.waitKey(int(1000 / FPS) if playing else 0) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                playing = not playing
            elif key == ord('r'):
                idx = 0
                playing = True
            if playing:
                idx = (idx + 1) % len(frames)
        cv2.destroyAllWindows()

    print(f"{'='*70}\n  Selesai!\n{'='*70}\n")


if __name__ == '__main__':
    main()