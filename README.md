# Red Color Segmentation using Classic Computer Vision

This repository contains a professional implementation of **Red Color Segmentation** using the **OpenCV** framework on a **Raspberry Pi 4B**. Unlike standard thresholding, this project utilizes advanced HSV color-space manipulation and morphological transformations to achieve high selectivity without the need for Deep Learning.

## 🚀 Technical Highlights
* **Dual-Range HSV Thresholding**: Red is uniquely cyclic in the Hue wheel. This project implements a dual-masking technique to capture both the start (0-10) and the end (170-180) of the Hue spectrum.
* **Morphological Refinement**: Applied **Opening** (erosion followed by dilation) and **Closing** to eliminate noise and bridge structural gaps.
* **Multi-Domain Generalization**: Validated across Automotive, Horticulture (Apples), and Botany (Strawberries) datasets.

## 📊 Quantitative Results
| Scenario | Automotive | Apples | Strawberries |
| :--- | :---: | :---: | :---: |
| **Default** | 9.16% | 41.88% | 11.85% |
| **Tight** | 3.77% | 3.60% | 7.96% |
| **Loose** | 10.26% | 54.69% | 12.81% |

## 🎨 Visual Results (Step-by-Step)
Below is the step-by-step visualization of the segmentation pipeline.

### 🚗 1. Automotive Dataset
**Original Input**
![Input](data/mobil.jpg)

**Binary Mask**
![Mask](output/output_mobil/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_mobil/03_result_default.jpg)

---

### 🍎 2. Apples Dataset
**Original Input**
![Input](data/apple.jpg)

**Binary Mask**
![Mask](output/output_apple/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_apple/03_result_default.jpg)

---

### 🍓 3. Strawberries Dataset
**Original Input**
![Input](data/strawberry.jpg)

**Binary Mask**
![Mask](output/output_strawberry/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_strawberry/03_result_default.jpg)

## 🎥 Demonstration
> 🔗 **[Watch Video Demonstration on YouTube](https://youtu.be/itw2XeYJprI?si=FVZCzmi9kIulS-zZ)**

## 📂 Project Documentation
* **[Technical Report](docs/006_Laporan%20Segmentasi%20Warna_Ahmad%20Hanif%20Abiyyu%20Khrisna.pdf)**
* **[Project Presentation](docs/006_PPT_Segmentasi%20Warna.pptx)**

---
**Author**: Ahmad Hanif Abiyyu Khrisna  
**Institution**: Electronic Engineering Polytechnic Institute of Surabaya (PENS)