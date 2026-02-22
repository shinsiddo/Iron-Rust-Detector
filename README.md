# Iron Rust Detector 🔍

An AI-based Iron Rust Detection system built using a Keras model trained with Google Teachable Machine and integrated into a Python GUI application.

## 📌 Project Overview

This project detects whether an iron surface contains rust using a trained deep learning model. The model was trained using Google Teachable Machine and exported as a Keras (.h5) model file.

The application uses a simple Python GUI to allow users to upload an image and get instant rust detection results.

---

## 🧠 Model Details

- Model Type: Keras (.h5)
- Trained Using: Google Teachable Machine
- Classification: Rust / No Rust
- Input: Image file
- Output: Predicted class with confidence

---

## 🛠️ Requirements

- Python 3.10

Install dependencies using:

```bash
pip install -r requirements.txt


PROJECT STRUCTURE:

Iron-Rust-Detector/
│
├── predict.py
├── keras_model.h5
├── labels.txt
├── requirements.txt
├── README.md
├── LICENSE