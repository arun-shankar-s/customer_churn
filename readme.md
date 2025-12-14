# 📡 Customer Churn Prediction System

An end-to-end **Machine Learning application** that predicts customer churn probability and explains *why* a customer is likely to leave.  
Built with **Python, Scikit-learn, FastAPI, Streamlit**, and deployed using **Railway & Streamlit Cloud**.

---

## 🚀 Live Demo

- **API (FastAPI – Railway):**  
  https://customerchurn-production.up.railway.app/docs

- **Web App (Streamlit):**  
  👉 Deployed via Streamlit Cloud
  https://customerchurn-1221.streamlit.app/

---

## 🧠 Problem Statement

Customer churn is a critical business problem where customers stop using a service.  
The goal of this project is to:

- Predict **churn probability**
- Identify **high-risk customers**
- Provide **actionable business insights**
- Deliver results via a **real-world deployed application**

---

## 🏗️ Project Architecture

User (Streamlit UI)
↓
FastAPI REST API
↓
ML Model (Logistic Regression)
↓
Churn Probability + Risk Insights

yaml
Copy code

---

## 🔍 Key Features

### ✅ Machine Learning
- Binary classification (Churn / No Churn)
- Logistic Regression baseline model
- Feature engineering & one-hot encoding
- Class imbalance handling
- Threshold tuning for recall optimization

### ✅ Explainability
- “Why this customer may churn” section
- Business-driven rules based on EDA insights:
  - Low tenure
  - Month-to-month contracts
  - High monthly charges
  - Electronic check payment
  - Lack of tech support
  - Senior citizen risk

### ✅ Deployment
- **FastAPI** for model serving
- **Railway** for backend deployment
- **Streamlit** for interactive UI
- Downloadable churn report (CSV)

---

## 📊 Model Performance (Baseline)

| Model | Accuracy | Precision (Churn) | Recall (Churn) | F1 |
|------|----------|------------------|---------------|----|
| Logistic Regression | ~0.80 | 0.65 | **0.55** | 0.60 |
| Random Forest | ~0.80 | 0.67 | 0.48 | 0.56 |

👉 Logistic Regression chosen for **better recall**, which is more important for churn detection.

---

## 🧪 API Usage Example

**Endpoint**
POST /predict


**Sample Request**
json
{
  "seniorcitizen": 0,
  "tenure": 12,
  "monthlycharges": 70.5,
  "totalcharges": 800.0,
  "gender": "Male",
  "partner": "Yes",
  "dependents": "No",
  "phoneservice": "Yes",
  "multiplelines": "No",
  "internetservice": "Fiber optic",
  "onlinesecurity": "No",
  "onlinebackup": "Yes",
  "deviceprotection": "No",
  "techsupport": "No",
  "streamingtv": "Yes",
  "streamingmovies": "Yes",
  "contract": "Month-to-month",
  "paperlessbilling": "Yes",
  "paymentmethod": "Electronic check"
}
Response


{
  "churn_probability": 0.76
}

---

🎨 Streamlit UI Highlights
Clean multi-section layout

Field explanations via expandable help panel

Churn probability metric

Churn reasoning explanation

Downloadable churn report

Custom background styling

🛠️ Tech Stack
Python

Pandas / NumPy

Scikit-learn

FastAPI

Streamlit

Joblib

Railway

Streamlit Cloud

📌 Future Improvements
SHAP-based explainability

Advanced models (XGBoost, LightGBM)

User authentication

Customer segmentation dashboard

Monitoring & drift detection

👤 Author
Arun
Machine Learning & AI Enthusiast
Built as a foundation ML project for real-world deployment & interviews.
