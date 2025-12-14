from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Load artifacts
model = joblib.load("models/logistic_regression_model.pkl")
columns = joblib.load("models/columns.pkl")
scaler = joblib.load("models/scaler.pkl")
num_cols = ['seniorcitizen', 'tenure', 'monthlycharges', 'totalcharges']

# Remove churn column from model input
columns = [c for c in columns if c != "churn"]

class ChurnInput(BaseModel):
    seniorcitizen: int
    tenure: float
    monthlycharges: float
    totalcharges: float
    gender: Optional[str] = None
    partner: Optional[str] = None
    dependents: Optional[str] = None
    phoneservice: Optional[str] = None
    multiplelines: Optional[str] = None
    internetservice: Optional[str] = None
    onlinesecurity: Optional[str] = None
    onlinebackup: Optional[str] = None
    deviceprotection: Optional[str] = None
    techsupport: Optional[str] = None
    streamingtv: Optional[str] = None
    streamingmovies: Optional[str] = None
    contract: Optional[str] = None
    paperlessbilling: Optional[str] = None
    paymentmethod: Optional[str] = None

@app.post("/predict")
def predict(input_data: ChurnInput):

    df = pd.DataFrame([input_data.dict()])
    df = pd.get_dummies(df)

    # Add missing columns
    for col in columns:
        if col not in df:
            df[col] = 0

    # Reorder
    df = df[columns]

    df[num_cols] = scaler.transform(df[num_cols])

    prob = model.predict_proba(df)[0][1]
    return {"churn_probability": float(prob)}
