# Red Color Segmentation using Classic Computer Vision

[cite_start]This repository contains a professional implementation of **Red Color Segmentation** using the **OpenCV** framework on a **Raspberry Pi 4B**[cite: 503, 539]. [cite_start]Unlike standard thresholding, this project utilizes advanced HSV color-space manipulation and morphological transformations to achieve high selectivity without the need for Deep Learning[cite: 531, 703].

## 🚀 Technical Highlights
* [cite_start]**Dual-Range HSV Thresholding**: Red is uniquely cyclic in the Hue wheel[cite: 533]. [cite_start]This project implements a dual-masking technique to capture both the start (0-10) and the end (170-180) of the Hue spectrum[cite: 535, 711, 712].
* [cite_start]**Morphological Refinement**: Applied **Opening** (erosion followed by dilation) to eliminate salt-and-pepper noise and **Closing** (dilation followed by erosion) to bridge structural gaps in the detected objects[cite: 565, 891].
* [cite_start]**Lighting Robustness**: Analyzed under simulated light and dim conditions ($0.4\times$ to $1.6\times$ Value factor) to evaluate threshold sensitivity[cite: 571, 589].
* [cite_start]**Multi-Domain Generalization**: Validated on three distinct datasets: Automotive (Toyota C-HR/Yaris), Horticulture (Apples), and Botany (Strawberries)[cite: 541, 542, 779, 780].

## 📊 Quantitative Results
[cite_start]The algorithm was benchmarked across various scenarios to evaluate detection accuracy (Red Pixel Ratio)[cite: 593, 629]:

| Scenario | Automotive | Apples | Strawberries | Characteristics |
| :--- | :---: | :---: | :---: | :--- |
| **Default** | 9.16% | 41.88% | 11.85% | [cite_start]Optimal baseline compromise [cite: 593, 629] |
| **Tight** | 3.77% | 3.60% | 7.96% | [cite_start]High selectivity, higher False Negatives [cite: 593, 629] |
| **Loose** | 10.26% | 54.69% | 12.81% | [cite_start]High sensitivity, higher False Positives [cite: 593, 629] |
| **Dim (0.4x V)** | 3.58% | 7.16% | 6.86% | [cite_start]Significant detection drop [cite: 593, 629] |

## 🎨 Visual Results (Default Scenario)
[cite_start]The following comparisons demonstrate the pipeline's effectiveness in isolating target red objects while rejecting non-target colors (e.g., white, yellow, and green)[cite: 578, 605, 620].

### 1. Automotive Dataset
| Input Image | Binary Mask | Segmentation Result |
| :---: | :---: | :---: |
| ![Input](data/mobil.jpg) | ![Mask](output/output_mobil/02_mask_default.jpg) | ![Result](output/output_mobil/03_result_default.jpg) |

### 2. Botanical Dataset (Apples & Strawberries)
| Input Image | Binary Mask | Segmentation Result |
| :---: | :---: | :---: |
| ![Input](data/apple.jpg) | ![Mask](output/output_apple/02_mask_default.jpg) | ![Result](output/output_apple/03_result_default.jpg) |
| ![Input](data/strawberry.jpg) | ![Mask](output/output_strawberry/02_mask_default.jpg) | ![Result](output/output_strawberry/03_result_default.jpg) |

## 🎥 Demonstration
Technical walkthrough and live simulation results are available on YouTube:
> [cite_start]🔗 **[Watch Video Demonstration](https://youtu.be/itw2XeYJprI?si=FVZCzmi9kIulS-zZ)** [cite: 775]

## 📂 Project Documentation
Full technical analysis and presentation slides are available in the `docs/` folder:
* [cite_start]**[Technical Report](docs/006_Laporan%20Segmentasi%20Warna_Ahmad%20Hanif%20Abiyyu%20Khrisna.pdf)**: Detailed methodology, HSV theory, and full experiment data[cite: 501].
* [cite_start]**[Project Presentation](docs/006_PPT_Segmentasi%20Warna.pptx)**: Visual summary of the pipeline and challenges[cite: 781].

## ⚙️ Requirements
* [cite_start]**Hardware**: Raspberry Pi 4B (aarch64) or compatible PC[cite: 539].
* [cite_start]**Software**: Python 3.11+, OpenCV 4.10.0, NumPy 2.2.4[cite: 540].

---
**Author**: Ahmad Hanif Abiyyu Khrisna  
[cite_start]**Institution**: Electronic Engineering Polytechnic Institute of Surabaya (PENS) [cite: 509]