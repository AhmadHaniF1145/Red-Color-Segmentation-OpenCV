# SCRIPT PENJELASAN PROGRAM `segmentasi_merah.py`
## Panduan Per-Baris untuk Memahami Setiap Bagian Kode

> Panduan ini menjelaskan kode `segmentasi_merah.py` baris demi baris.
> Untuk setiap bagian: **apa fungsinya, mengapa ditulis seperti itu, dan teori di baliknya.**
> Cocok dipakai saat presentasi atau sebagai bahan studi mandiri.

---

## BAGIAN 1: IMPORT MODULES

```python
import cv2
import numpy as np
import os
import argparse
```

### Penjelasan per modul:

**`import cv2`**
- Library OpenCV (Open Source Computer Vision Library)
- Berisi semua fungsi pengolahan citra: `cv2.imread`, `cv2.cvtColor`, `cv2.inRange`, dll
- Asalnya dari proyek Intel tahun 1999, sekarang open-source
- Versi yang kita pakai: OpenCV 4.10.0
- **Mengapa diberi alias `cv2`?** Konvensi internasional sejak versi 2.x — tidak bisa diubah

**`import numpy as np`**
- NumPy adalah library numerik fundamental Python
- Citra di OpenCV **direpresentasikan sebagai NumPy array**, bukan struktur khusus OpenCV
- Alias `np` adalah konvensi standar
- Kita pakai NumPy untuk: bikin array threshold (`np.array(...)`), kernel morfologi (`np.ones(...)`), hitung piksel non-zero (`np.count_nonzero`), clip nilai (`np.clip`)

**`import os`**
- Library standar Python untuk operasi filesystem
- Kita gunakan untuk: bikin folder output (`os.makedirs`)
- Alasan pakai `os` daripada manual: cross-platform (Windows, Linux, macOS)

**`import argparse`**
- Library untuk **parsing command-line arguments**
- Memungkinkan script dipanggil dengan parameter: `python segmentasi_merah.py --input mobil.jpg --outdir output`
- Lebih profesional daripada hardcode nama file di dalam script

---

## BAGIAN 2: PARAMETER GLOBAL (HSV Ranges)

```python
LOWER_RED_1 = np.array([  0, 120,  70])
UPPER_RED_1 = np.array([ 10, 255, 255])
LOWER_RED_2 = np.array([170, 120,  70])
UPPER_RED_2 = np.array([180, 255, 255])
```

### Penjelasan:

Empat baris ini adalah **batas threshold untuk warna merah** di ruang HSV.

**Format `np.array([H, S, V])`:**
- Indeks 0 = Hue
- Indeks 1 = Saturation
- Indeks 2 = Value

**Mengapa ada 4 array (2 lower + 2 upper)?**

Karena warna merah di HSV **terbagi menjadi 2 rentang Hue**:
- **Rentang 1: Hue 0-10** → "merah awal" (merah pure menuju merah-jingga)
- **Rentang 2: Hue 170-180** → "merah akhir" (merah-magenta menuju merah pure)

Hue bersifat **siklis**: 0° dan 360° adalah warna yang sama (merah). Karena OpenCV memetakan Hue ke 0-179 (bukan 0-359 untuk muat di uint8), titik "putus"-nya ada di sekitar 0 dan 179.

**Mengapa Saturation minimal 120, Value minimal 70?**
- **S < 120** = warna kelabu/pucat → bukan merah jelas
- **V < 70** = piksel terlalu gelap (mendekati hitam) → tidak reliable

Nilai ini hasil **tuning empiris** yang umum digunakan di tutorial OpenCV. Kalau diubah, hasil berubah (lihat skenario Tight & Loose).

**Mengapa pakai `np.array` bukan list Python biasa `[0, 120, 70]`?**

`cv2.inRange()` menerima list biasa, **tetapi** menggunakan `np.array` lebih cepat karena tidak ada konversi internal. Ini best practice di OpenCV.

```python
KERNEL = np.ones((5, 5), np.uint8)
```

**Penjelasan:**
- Kernel adalah **structuring element** untuk operasi morfologi
- `np.ones((5, 5))` = matriks 5×5 berisi semua angka 1
- `np.uint8` = tipe data 8-bit unsigned integer (sesuai kebutuhan OpenCV)
- Ukuran 5×5 dipilih karena **proporsional dengan ukuran citra 800-piksel**
- Kernel terlalu kecil → cleanup tidak efektif
- Kernel terlalu besar → objek penting bisa terhapus

---

## BAGIAN 3: FUNCTION `segment_red()`

```python
def segment_red(img_bgr,
                low1=LOWER_RED_1, up1=UPPER_RED_1,
                low2=LOWER_RED_2, up2=UPPER_RED_2,
                use_morph=True):
```

### Penjelasan signature:

- `img_bgr` — citra input dalam format BGR (output dari `cv2.imread`)
- `low1, up1, low2, up2` — parameter threshold dengan **default value**. Bisa override saat panggil function untuk skenario tight/loose
- `use_morph=True` — flag boolean untuk on/off morfologi

**Mengapa pakai default value?**
- Bisa dipanggil simple: `segment_red(img)` → pakai default
- Bisa di-override: `segment_red(img, low1=np.array([0, 200, 100]), ...)` → tight
- Pattern ini disebut **keyword arguments** di Python

```python
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
```

### Penjelasan:

**`cv2.cvtColor(src, code)`** = konversi ruang warna.

**Tahap 1 dari pipeline.**

- `src` = citra sumber (BGR)
- `code = cv2.COLOR_BGR2HSV` = kode konversi BGR → HSV

**Mengapa BGR2HSV bukan RGB2HSV?**

Karena OpenCV **default membaca file dalam format BGR**, bukan RGB. Ini warisan sejarah dari awal pengembangan OpenCV oleh Intel. Kalau pakai RGB2HSV, hasilnya akan salah (kanal R dan B tertukar).

**Apa output dari `cv2.cvtColor`?**

NumPy array dengan shape sama (H, W, 3) tapi nilai-nya sekarang adalah HSV. Kanal:
- `hsv[:,:,0]` = Hue (0-179)
- `hsv[:,:,1]` = Saturation (0-255)
- `hsv[:,:,2]` = Value (0-255)

```python
    mask1 = cv2.inRange(hsv, low1, up1)
    mask2 = cv2.inRange(hsv, low2, up2)
```

### Penjelasan:

**`cv2.inRange(src, lowerb, upperb)`** = thresholding per-piksel-per-kanal.

**Tahap 2 dari pipeline.**

Untuk setiap piksel `p` di `hsv`:
- Jika `lowerb[0] ≤ p[0] ≤ upperb[0]` AND `lowerb[1] ≤ p[1] ≤ upperb[1]` AND `lowerb[2] ≤ p[2] ≤ upperb[2]`
- Maka piksel di mask = **255** (putih)
- Selain itu = **0** (hitam)

**Output:** citra biner (mask) dengan tipe uint8, shape (H, W).

**Kita panggil 2 kali** karena ada 2 rentang Hue merah:
- `mask1` = piksel yang merah-awal (Hue 0-10)
- `mask2` = piksel yang merah-akhir (Hue 170-180)

```python
    mask = cv2.bitwise_or(mask1, mask2)
```

### Penjelasan:

**`cv2.bitwise_or(src1, src2)`** = operasi OR per-bit.

**Tahap 3 dari pipeline.**

Untuk setiap piksel:
- `mask[i,j] = mask1[i,j] | mask2[i,j]`
- Kalau **salah satu** mask aktif (255), maka hasil aktif
- Kalau **keduanya** 0, hasil 0

**Mengapa OR, bukan AND?**

Kita ingin **menggabungkan**: piksel valid kalau dia merah-awal **ATAU** merah-akhir. Bukan "harus dua-duanya".

Hasilnya: satu mask utuh yang berisi seluruh spektrum merah.

```python
    if use_morph:
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  KERNEL, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)
```

### Penjelasan:

**`cv2.morphologyEx(src, op, kernel, iterations=...)`** = operasi morfologi advanced.

**Tahap 4 dari pipeline (cleanup).**

**`MORPH_OPEN`** = Opening = **erosi diikuti dilasi**.

- **Erosi**: untuk setiap piksel, lihat tetangga 5×5. Kalau **ada satu saja yang 0**, piksel jadi 0
- **Dilasi**: untuk setiap piksel, lihat tetangga 5×5. Kalau **ada satu saja yang 255**, piksel jadi 255

Efek bersihnya: **menghilangkan bercak putih kecil** (noise/false positive).

**`MORPH_CLOSE`** = Closing = **dilasi diikuti erosi**.

Efeknya kebalikan: **menutup lubang hitam kecil di dalam objek putih** (false negative).

**Mengapa OPEN dulu, lalu CLOSE?**
- Bersihkan noise dulu, supaya CLOSE tidak ikut menggabungkan noise dengan objek utama
- Lalu CLOSE untuk meratakan permukaan objek dan menutup lubang internal

**Mengapa CLOSE iterations=2?**
- 1 iterasi kadang tidak cukup untuk lubang yang lebih besar
- 2 iterasi memberi efek closing lebih agresif tanpa merusak bentuk asli

```python
    result = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
    return mask, result
```

### Penjelasan:

**`cv2.bitwise_and(src1, src2, mask=...)`** = operasi AND per-bit dengan mask.

**Tahap 5 dari pipeline (output).**

**Pattern khusus**: `bitwise_and(img, img, mask=mask)` — operand pertama dan kedua **sama-sama citra asli**, parameter `mask` menentukan piksel mana yang dilewati.

Hasilnya: citra asli yang **hanya menampilkan piksel pada area mask aktif**, sisanya jadi hitam.

**Mengapa pattern ini umum?**
- AND antara dua citra identik = citra itu sendiri (jadi hasil tidak berubah di area mask aktif)
- Parameter `mask` kemudian melakukan filter di area non-aktif → jadi hitam

`return mask, result` — function mengembalikan **dua nilai**: mask biner dan citra hasil segmentasi.

---

## BAGIAN 4: FUNCTION `adjust_brightness()`

```python
def adjust_brightness(img, factor):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 2] = np.clip(hsv[..., 2] * factor, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
```

### Penjelasan:

Fungsi ini **mensimulasikan perubahan pencahayaan** untuk eksperimen Bright/Dim.

**Baris 1:**
- Konversi BGR → HSV
- `.astype(np.float32)` — ubah tipe data ke float32

**Mengapa float32?** Karena kita akan **kalikan dengan faktor desimal** (1.6 atau 0.4). Kalau tetap uint8, hasilnya akan **truncated** (1.6 jadi 1, hilang ketelitian).

**Baris 2:**
- `hsv[..., 2]` — akses kanal Value saja (kanal indeks 2)
- `* factor` — kalikan dengan faktor (1.6 untuk bright, 0.4 untuk dim)
- `np.clip(..., 0, 255)` — batasi nilai antara 0-255 (mencegah overflow)

**Mengapa `[..., 2]` bukan `[:, :, 2]`?**

`...` (ellipsis) adalah **wildcard** untuk semua dimensi sebelumnya. Sama dengan `[:, :, 2]` tapi lebih singkat. Standar di NumPy.

**Baris 3:**
- `.astype(np.uint8)` — kembalikan tipe data ke uint8 (sesuai format OpenCV)
- Konversi HSV → BGR untuk ditampilkan/disimpan

**Mengapa kalkulasi di kanal V, bukan tambah saja?**

- Kalau kita `+ 50` pada V, 200 jadi 250 (mendekati maksimum) — efeknya kecil
- Kalau kita `* 1.6`, 200 jadi 320 (clipped ke 255) — efek sama
- Tapi 100 → `+50 = 150` vs `*1.6 = 160` — proportional adjustment
- **Multiplicative adjustment lebih natural** untuk simulasi perubahan iluminasi

---

## BAGIAN 5: FUNCTION `red_pixel_ratio()`

```python
def red_pixel_ratio(mask):
    return 100.0 * np.count_nonzero(mask) / mask.size
```

### Penjelasan:

Hitung **persentase piksel aktif** di mask.

- `np.count_nonzero(mask)` = jumlah piksel yang **bukan 0** (yaitu yang 255)
- `mask.size` = total jumlah piksel (H × W)
- `* 100.0` = ubah ke persentase
- `100.0` (float) memastikan hasilnya float, bukan integer division

**Mengapa metric ini penting?**
- Cara mudah membandingkan hasil antar skenario
- Tapi **bukan ukuran akurasi**! Bisa misleading kalau citra punya komposisi berbeda

**Contoh:**
- Mobil default: 9.16% (banyak ruang putih kosong)
- Apel default: 41.88% (memang banyak area merah)
- **Bukan** berarti apel "lebih akurat dari mobil"!

---

## BAGIAN 6: FUNCTION `main()`

```python
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input',  default='mobil.jpg')
    ap.add_argument('--outdir', default='output')
    ap.add_argument('--width',  type=int, default=800)
    args = ap.parse_args()
```

### Penjelasan argparse:

- `argparse.ArgumentParser()` — bikin parser
- `add_argument('--input', default='mobil.jpg')` — definisikan opsi `--input` dengan default
- `args = ap.parse_args()` — parse argumen dari command line

**Cara pakai dari terminal:**
```bash
python3 segmentasi_merah.py --input apple.jpg --outdir output_apple --width 900
```

Kalau tidak diberi argumen, akan pakai default: `mobil.jpg`, `output`, `800`.

**Mengapa width default 800?**

Resize ke 800 piksel untuk **efisiensi di Raspberry Pi**. Citra original bisa 4000×3000 piksel (12 megapiksel), terlalu besar untuk diproses real-time. 800 piksel cukup untuk segmentasi warna.

```python
    os.makedirs(args.outdir, exist_ok=True)
    img = cv2.imread(args.input)
    if img is None:
        raise FileNotFoundError(f"Tidak dapat membaca {args.input}")
```

### Penjelasan:

- `os.makedirs(folder, exist_ok=True)` — bikin folder. Flag `exist_ok=True` artinya **tidak error** kalau folder sudah ada
- `cv2.imread(filename)` — baca file gambar. Mengembalikan NumPy array atau `None` kalau gagal
- `if img is None` — pengecekan eksplisit. **Sangat penting!** Kalau filename salah, OpenCV tidak melempar exception, dia hanya mengembalikan None

```python
    if args.width > 0 and img.shape[1] > args.width:
        scale = args.width / img.shape[1]
        img = cv2.resize(img, (args.width, int(img.shape[0] * scale)),
                         interpolation=cv2.INTER_AREA)
```

### Penjelasan resize:

- `img.shape` = `(height, width, channels)` — ingat **height duluan** di NumPy
- `img.shape[1]` = width asli
- `scale = target_width / original_width` — rasio scaling
- `cv2.resize(img, (new_w, new_h), interpolation=...)` — resize. **Perhatikan urutan: width duluan di tuple ukuran target!**
- `interpolation=cv2.INTER_AREA` — algoritma interpolasi terbaik untuk **memperkecil**. Untuk memperbesar, pakai `INTER_CUBIC` atau `INTER_LINEAR`

```python
    mask, res = segment_red(img)
    cv2.imwrite(f'{args.outdir}/01_original.jpg', img)
    cv2.imwrite(f'{args.outdir}/02_mask_default.jpg', mask)
    cv2.imwrite(f'{args.outdir}/03_result_default.jpg', res)
    print(f"[Default ]  Red ratio = {red_pixel_ratio(mask):6.2f}%")
```

### Penjelasan:

- `segment_red(img)` — panggil pipeline default
- `cv2.imwrite(filename, image)` — simpan gambar ke file. Format ditentukan dari ekstensi
- `f'...'` — **f-string** (formatted string), Python 3.6+
- `:6.2f` — format spec: minimal 6 karakter, 2 digit desimal

```python
    # Tight scenario
    mask_t, res_t = segment_red(
        img,
        low1=np.array([0,   200, 100]), up1=np.array([8,   255, 255]),
        low2=np.array([172, 200, 100]), up2=np.array([180, 255, 255]))
```

### Penjelasan tight scenario:

- Override default parameters dengan threshold yang **lebih ketat**:
  - S minimal: 120 → 200 (hanya warna sangat jenuh)
  - V minimal: 70 → 100 (hanya warna cukup terang)
  - Hue 1 max: 10 → 8 (rentang lebih sempit)
  - Hue 2 min: 170 → 172 (rentang lebih sempit)

**Hasil prediksi:** rasio piksel **turun drastis** karena banyak yang gagal lolos.

```python
    # Loose scenario
    mask_l, res_l = segment_red(
        img,
        low1=np.array([0,   60, 40]),  up1=np.array([15,  255, 255]),
        low2=np.array([160, 60, 40]),  up2=np.array([180, 255, 255]))
```

### Penjelasan loose scenario:

Kebalikan dari tight—threshold dilonggarkan:
- S minimal: 120 → 60 (warna pucat ikut lolos)
- V minimal: 70 → 40 (area gelap kemerahan ikut lolos)
- Rentang Hue dilebarkan ke 0-15 dan 160-180

**Hasil prediksi:** rasio piksel **naik** karena lebih banyak piksel lolos. Tapi sebagian besar kenaikan adalah **false positive**.

```python
    # Bright & Dim scenarios
    bright = adjust_brightness(img, 1.6)
    dim    = adjust_brightness(img, 0.4)
    mb, rb = segment_red(bright)
    md, rd = segment_red(dim)
    cv2.imwrite(f'{args.outdir}/08_bright_input.jpg', bright)
    cv2.imwrite(f'{args.outdir}/09_bright_mask.jpg',  mb)
    cv2.imwrite(f'{args.outdir}/10_dim_input.jpg',    dim)
    cv2.imwrite(f'{args.outdir}/11_dim_mask.jpg',     md)
```

### Penjelasan:

- Modifikasi citra dengan `adjust_brightness` (tahap simulasi)
- Lalu jalankan `segment_red()` dengan **threshold default** (yang berubah hanya inputnya)
- Save kedua input (untuk dokumentasi) dan mask hasilnya

**Mengapa input bright/dim juga disimpan?**

Untuk **bukti visual** di laporan: "ini lho, citra yang diproses, dan ini hasilnya". Tanpa input visual, audiens tidak bisa membayangkan kondisi pencahayaan yang disimulasikan.

```python
if __name__ == '__main__':
    main()
```

### Penjelasan:

**Idiom Python standar.** Hanya jalankan `main()` kalau script di-run langsung, bukan di-import sebagai module.

`__name__` adalah variabel built-in:
- Kalau script dijalankan langsung: `__name__ == '__main__'`
- Kalau di-import: `__name__ == 'segmentasi_merah'` (nama file tanpa .py)

---

## TIPS UNTUK PERTANYAAN DOSEN

**Q: Kenapa nilai threshold pakai (120, 70) dan bukan angka lain?**
> Hasil eksperimen empiris di berbagai tutorial OpenCV. S=120 cukup untuk membedakan merah jenuh dari abu-abu, V=70 cukup untuk mengabaikan piksel hampir hitam. Bisa di-tune sesuai kondisi citra.

**Q: Bisakah pakai metode lain selain HSV?**
> Bisa. Ruang warna **Lab** (kanal a* untuk merah-hijau) atau **YCbCr** juga bisa. HSV dipilih karena paling intuitif dan banyak referensinya. Combining HSV + Lab bahkan bisa meningkatkan akurasi.

**Q: Kenapa kernel morfologi 5×5?**
> Proporsional dengan ukuran citra 800 piksel. Untuk citra lebih besar (1920×1080), bisa pakai 7×7 atau 9×9. Aturan praktis: kira-kira 1% dari sisi terpendek.

**Q: Apa beda erosi dan dilasi?**
> Erosi mengkikis tepi objek (bikin lebih kecil); dilasi memperluas tepi objek (bikin lebih besar). Kombinasi keduanya menghasilkan operasi advanced seperti OPEN dan CLOSE.

**Q: Apa kelemahan algoritma ini?**
> Tidak memahami bentuk—hanya warna. Benda merah selain target (rambu, lampu rem, baju merah) ikut terdeteksi. Solusinya: filter kontur geometris, ROI, atau kombinasi multi-color space.

**Q: Berapa lama eksekusinya di Raspberry Pi?**
> Untuk citra 800×450 di RPi 4B: sekitar 5-10 ms total (~100-200 FPS). Cocok untuk aplikasi real-time embedded vision.

**Q: Mengapa pakai OpenCV bukan PIL/Pillow?**
> OpenCV lebih cepat dan lengkap untuk computer vision. PIL/Pillow lebih cocok untuk image manipulation umum (resize, format conversion). Untuk segmentasi & deteksi, OpenCV adalah pilihan utama.

**Q: Bedanya `cv2.threshold` vs `cv2.inRange`?**
> `cv2.threshold` untuk **single-channel** (grayscale), threshold di satu nilai. `cv2.inRange` untuk **multi-channel** (BGR/HSV), threshold dengan rentang min-max per kanal. Untuk warna, harus pakai `inRange`.

**Q: Apa itu Hough Transform yang disebut di solusi?**
> Algoritma untuk mendeteksi bentuk geometris (garis, lingkaran). Bisa dipakai untuk **validasi** setelah segmentasi warna—misal, mendeteksi roda mobil di dalam blob merah untuk memastikan itu mobil, bukan rambu.

---

## RINGKASAN PIPELINE

| Tahap | Fungsi OpenCV | Input → Output |
|-------|---------------|----------------|
| 1 | `cv2.imread` | File → Array BGR |
| 2 | `cv2.cvtColor` | BGR → HSV |
| 3 | `cv2.inRange` (×2) | HSV + threshold → 2 mask biner |
| 4 | `cv2.bitwise_or` | 2 mask → 1 mask gabungan |
| 5 | `cv2.morphologyEx` (OPEN+CLOSE) | mask kotor → mask bersih |
| 6 | `cv2.bitwise_and` | mask + citra asli → hasil segmentasi |
| 7 | `cv2.imwrite` | Array → File |

---

**Selamat mempelajari! Semoga sukses presentasinya 🎯**