
# AI-POWERED CAREER GUIDENCE SYSTEM

🎯 A machine learning-based web application that predicts career paths based on user inputs using a trained model.

---

## 📑 Table of Contents

* Overview
* Features
* Tech Stack
* Installation
* Usage
* Model Training
* File Structure
* Contributors

---

## 🔍 Overview

CCP2 is a machine learning project that assists users in identifying suitable career paths based on various input features. The backend is built in Python and uses trained ML models to give predictions.

---

## ✨ Features

* Career prediction using trained ML model
* Interactive user input interface (via `app.py`)
* Label encoding for categorical variables
* Model training script (`train_model.py`)
* Persistent model storage using `pickle`

---

## 🛠️ Tech Stack

* **Programming Language**: Python 3
* **Libraries**: `scikit-learn`, `pandas`, `pickle`
* **Model Type**: Supervised classification
* **Frontend**:  Flask 

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/HarshanaRK/AI_Career_Guidance_System_ccp.git
   cd AI_Career_Guidance_System_ccp
   ```

2. **Install dependencies**

   Install required packages:

   ```
   pip install 
   ```

3. **Set up environment variables**
   Create a `.env` file and add any required keys or secrets

---

## ▶️ Usage

To run the application:

```
python app.py
```

This starts the prediction interface, which allows users to input details and receive career suggestions.

---

## 🧠 Model Training

If you wish to retrain the model:

1. Place your training dataset as `dataset9000.csv` or modify the path in `train_model.py`.
2. Run:

```
python train_model.py
```

This will generate updated versions of `careerlast.pkl` and `label_encoder.pkl`.

---

## 📂 File Structure

```
AI_Career_Guidance_System
│
├── app.py                 # Main application file
├── model.py               # ML model logic
├── train_model.py         # Model training script
├── test_pickle.py         # Pickle file testing script
├── careerlast.pkl         # Trained model
├── label_encoder.pkl      # Encoded labels
├── dataset9000.csv        # Dataset file
├── .env                   # Environment variables (not tracked)
├── .gitignore             # Git ignore rules
```

---

## 👥 Contributors

* Harshana R K
* Vishal LSK

---
