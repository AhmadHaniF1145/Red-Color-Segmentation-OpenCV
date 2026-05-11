# Red Color Segmentation using Classic Computer Vision

This repository contains a professional implementation of **Red Color Segmentation** using the **OpenCV** framework on a **Raspberry Pi 4B**. Unlike standard thresholding, this project utilizes advanced HSV color-space manipulation and morphological transformations to achieve high selectivity without the need for Deep Learning.

## 🚀 Technical Highlights
* **Dual-Range HSV Thresholding**: Red is uniquely cyclic in the Hue wheel. This project implements a dual-masking technique to capture both the start (0-10) and the end (170-180) of the Hue spectrum.
* **Morphological Refinement**: Applied **Opening** (erosion followed by dilation) to eliminate salt-and-pepper noise and **Closing** (dilation followed by erosion) to bridge structural gaps in the detected objects.
* **Lighting Robustness**: Simulated across various Value ($V$) factors ($0.4\times$ to $1.6\times$) to analyze threshold sensitivity under realistic lighting conditions.
* **Multi-Domain Generalization**: Validated on three distinct datasets: Automotive (Toyota C-HR/Yaris), Horticulture (Apples), and Botany (Strawberries).

## 📊 Quantitative Results
The algorithm was benchmarked across three threshold scenarios (Default, Tight, Loose) to evaluate the trade-off between *False Positives* and *False Negatives*.

| Scenario | Automotive | Apples | Strawberries | Characteristics |
| :--- | :---: | :---: | :---: | :--- |
| **Default** | 9.16% | 41.88% | 11.85% | Optimal baseline compromise |
| **Tight** | 3.77% | 3.60% | 7.96% | High selectivity, higher False Negatives |
| **Loose** | 10.26% | 54.69% | 12.81% | High sensitivity, higher False Positives |
| **Dim (0.4x V)** | 3.58% | 7.16% | 6.86% | Significant detection drop |

## 🎥 Demonstration
Technical walkthrough and live simulation results are available on YouTube:
> 🔗 **[Watch Video Demonstration](YOUR_YOUTUBE_LINK_HERE)**

## 📂 Project Documentation
To maintain high engineering standards, this repository includes full technical documentation:
* [cite_start]**[Technical Report](docs/006_Laporan%20Segmentasi%20Warna_Ahmad%20Hanif%20Abiyyu%20Khrisna.pdf)**: Comprehensive analysis of HSV theory, methodology, and results[cite: 1, 10, 13, 176].
* [cite_start]**[Project Presentation](docs/006_PPT_Segmentasi%20Warna.pptx)**: Visual summary of the pipeline and challenges[cite: 275, 278, 281].

## 🛠️ Repository Structure
* `src/`: Main Python implementation (`segmentasi_merah.py`).
* `data/`: Sample input datasets for replication.
* `requirements.txt`: Environment dependencies.

## ⚙️ Requirements
* **Hardware**: Raspberry Pi 4B (aarch64) or compatible PC.
* **Software**: Python 3.11+, OpenCV 4.10.0, NumPy 2.2.4.

---
**Author**: Ahmad Hanif Abiyyu Khrisna  
**Institution**: Electronic Engineering Polytechnic Institute of Surabaya (PENS)