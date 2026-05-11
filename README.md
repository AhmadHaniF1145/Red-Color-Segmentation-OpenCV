# Red Color Segmentation using Classic Computer Vision

This repository contains a professional implementation of **Red Color Segmentation** using the **OpenCV** framework on a **Raspberry Pi 4B**. [cite_start]Unlike standard thresholding, this project utilizes advanced HSV color-space manipulation and morphological transformations to achieve high selectivity without the need for Deep Learning[cite: 504, 540, 703].

## 🚀 Technical Highlights
* **Dual-Range HSV Thresholding**: Red is uniquely cyclic in the Hue wheel. [cite_start]This project implements a dual-masking technique to capture both the start (0-10) and the end (170-180) of the Hue spectrum[cite: 535, 551].
* [cite_start]**Morphological Refinement**: Applied **Opening** (erosion followed by dilation) and **Closing** to eliminate noise and bridge structural gaps[cite: 555, 556].
* [cite_start]**Multi-Domain Generalization**: Validated across Automotive, Horticulture (Apples), and Botany (Strawberries) datasets[cite: 596, 650].

## 📊 Quantitative Results (Red Pixel Ratio)
| Scenario | Automotive | Apples | Strawberries |
| :--- | :---: | :---: | :---: |
| **Default** | 9.16% | 41.88% | 11.85% |
| **Tight** | 3.77% | 3.60% | 7.96% |
| **Loose** | 10.26% | 54.69% | 12.81% |

[cite_start][cite: 593, 629]

## 🎨 Visual Results (Step-by-Step Visualization)
[cite_start]The following results demonstrate the pipeline's effectiveness using the **Default** scenario parameters[cite: 568].

### 🚗 1. Automotive Dataset
**Original Input Image**
![Input](data/mobil.jpg)

**Binary Mask (Identified Red Pixels)**
![Mask](output/output_mobil/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_mobil/03_result_default.jpg)

---

### 🍎 2. Apples Dataset
**Original Input Image**
![Input](data/apple.jpg)

**Binary Mask (Identified Red Pixels)**
![Mask](output/output_apple/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_apple/03_result_default.jpg)

---

### 🍓 3. Strawberries Dataset
**Original Input Image**
![Input](data/strawberry.jpg)

**Binary Mask (Identified Red Pixels)**
![Mask](output/output_strawberry/02_mask_default.jpg)

**Final Segmentation Result**
![Result](output/output_strawberry/03_result_default.jpg)

## 🎥 Demonstration
Technical walkthrough and live simulation results are available on YouTube:
> [cite_start]🔗 **[Watch Video Demonstration](https://youtu.be/itw2XeYJprI?si=FVZCzmi9kIulS-zZ)** [cite: 775]

## 📂 Project Documentation
* [cite_start]**[Technical Report](docs/006_Laporan%20Segmentasi%20Warna_Ahmad%20Hanif%20Abiyyu%20Khrisna.pdf)** [cite: 501]
* [cite_start]**[Project Presentation](docs/006_PPT_Segmentasi%20Warna.pptx)** [cite: 781]

---
**Author**: Ahmad Hanif Abiyyu Khrisna  
[cite_start]**Institution**: Electronic Engineering Polytechnic Institute of Surabaya (PENS) [cite: 506, 509]