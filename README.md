# Red Color Segmentation using Classic Computer Vision

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10-green?logo=opencv)](https://opencv.org/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4B-red?logo=raspberry-pi)](https://www.raspberrypi.com/)

This repository contains a high-performance **Red Color Segmentation** system implemented using **OpenCV** on **Raspberry Pi 4B**. By utilizing dual-range HSV thresholding and morphological refinement, this project achieves high selectivity in isolating red objects across diverse environments.

## 🚀 Technical Highlights
* **Dual-Range HSV Thresholding**: Implements a dual-masking technique to capture both ends of the Red Hue spectrum (0-10 and 170-180).
* **Morphological Refinement**: Uses **Opening** and **Closing** operations to eliminate salt-and-pepper noise and bridge structural gaps.
* **Lighting Robustness**: Tested under various light factors (0.4x to 1.6x Value) to ensure stability in different environments.
* **Multi-Domain Validation**: Proven effective on Automotive, Horticulture (Apples), and Botany (Strawberries) datasets.

## 📊 Quantitative Results (Red Pixel Ratio)
| Scenario | Automotive | Apples | Strawberries |
| :--- | :---: | :---: | :---: |
| **Default** | 9.16% | 41.88% | 11.85% |
| **Tight** | 3.77% | 3.60% | 7.96% |
| **Loose** | 10.26% | 54.69% | 12.81% |

## 🎨 Visual Results (Step-by-Step)
Below is the vertical showcase of the segmentation pipeline results.

### 🚗 1. Automotive Dataset
**Original Input Image**
![Input](data/mobil.jpg)

**Binary Mask**
![Mask](output/output_mobil/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_mobil/03_result_default.jpg)

---

### 🍎 2. Apples Dataset
**Original Input Image**
![Input](data/apple.jpg)

**Binary Mask**
![Mask](output/output_apple/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_apple/03_result_default.jpg)

---

### 🍓 3. Strawberries Dataset
**Original Input Image**
![Input](data/strawberry.jpg)

**Binary Mask**
![Mask](output/output_strawberry/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_strawberry/03_result_default.jpg)

## 🎥 Video Demonstration
Click the thumbnail below to watch the technical walkthrough and live simulation:

[![Watch the video](https://img.youtube.com/vi/4HHr_mnW15U/maxresdefault.jpg)](https://youtu.be/4HHr_mnW15U)

## 📄 Project Documentation
Explore the full technical analysis and presentation slides:
* 📑 **[Technical Report (PDF)](docs/006_Laporan%20Segmentasi%20Warna_Ahmad%20Hanif%20Abiyyu%20Khrisna.pdf)** - Detailed methodology, theory, and experimental data.
* 📊 **[Project Presentation (PPTX)](docs/006_PPT_Segmentasi%20Warna.pptx)** - Visual summary of the project pipeline and results.

---
**Author**: Ahmad Hanif Abiyyu Khrisna  
**Institution**: Electronic Engineering Polytechnic Institute of Surabaya (PENS)