import streamlit as st
import requests
import pandas as pd

API_URL = "https://customerchurn-production.up.railway.app/predict"

st.set_page_config(page_title="Customer Churn Predictor", layout="centered")

st.title("📡 Customer Churn Prediction App")
st.caption("Predict the likelihood of a customer leaving and understand why.")
st.caption("Predict the probability of a customer cancelling their subscription")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            135deg,
            #0f2027,
            #203a43,
            #2c5364
        );
        color: white;
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }

    div[data-testid="stMetricValue"] {
        color: #00ffcc !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- HELP SECTION ----------
with st.expander("ℹ️ What do these fields mean?"):
    st.markdown("""
    **Senior Citizen** – Whether the customer is a senior citizen.  
    **Tenure** – Number of months the customer has stayed with the company.  
    **Monthly Charges** – Monthly bill amount.  
    **Total Charges** – Total amount paid so far.  
    **Partner** – Whether the customer has a spouse/partner.  
    **Dependents** – Whether the customer has dependents (children/family).  
    **Contract** – Length of subscription commitment.  
    **Payment Method** – How the customer pays their bills.  
    """)

# -------------------------------
# INPUT SECTIONS
# -------------------------------
st.subheader("👤 Customer Profile")

col1, col2 = st.columns(2)
with col1:
    seniorcitizen = st.selectbox("Senior Citizen", [0, 1])
    gender = st.selectbox("Gender", ["Male", "Female"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])

with col2:
    tenure = st.number_input("Tenure (months)", 0, 72, 12)
    phoneservice = st.selectbox("Phone Service", ["Yes", "No"])
    multiplelines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

st.subheader("🌐 Services & Contract")

col3, col4 = st.columns(2)
with col3:
    internetservice = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    onlinesecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    techsupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])

with col4:
    streamingtv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streamingmovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

st.subheader("💳 Billing & Payment")

col5, col6 = st.columns(2)
with col5:
    monthlycharges = st.number_input("Monthly Charges", 0.0, 200.0, 70.5)
    totalcharges = st.number_input("Total Charges", 0.0, 10000.0, 800.0)

with col6:
    paperlessbilling = st.selectbox("Paperless Billing", ["Yes", "No"])
    paymentmethod = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )

# -------------------------------
# PREDICTION
# -------------------------------
if st.button("🚀 Predict Churn Probability"):

    payload = {
        "seniorcitizen": seniorcitizen,
        "tenure": tenure,
        "monthlycharges": monthlycharges,
        "totalcharges": totalcharges,
        "gender": gender,
        "partner": partner,
        "dependents": dependents,
        "phoneservice": phoneservice,
        "multiplelines": multiplelines,
        "internetservice": internetservice,
        "onlinesecurity": onlinesecurity,
        "onlinebackup": "Yes",
        "deviceprotection": "Yes",
        "techsupport": techsupport,
        "streamingtv": streamingtv,
        "streamingmovies": streamingmovies,
        "contract": contract,
        "paperlessbilling": paperlessbilling,
        "paymentmethod": paymentmethod
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        prob = response.json()["churn_probability"]

        st.markdown("---")
        st.metric("📊 Churn Probability", f"{prob:.2f}")

        # -------------------------------
        # 🧠 WHY THIS CUSTOMER MAY CHURN
        # -------------------------------
        st.subheader("🧠 Why this customer may churn")

        reasons = []

        if tenure < 12:
            reasons.append("Low tenure – customers often churn early.")
        if contract == "Month-to-month":
            reasons.append("Month-to-month contract shows weak commitment.")
        if monthlycharges > 70:
            reasons.append("High monthly charges indicate price sensitivity.")
        if paymentmethod == "Electronic check":
            reasons.append("Electronic check users historically churn more.")
        if techsupport == "No":
            reasons.append("Lack of tech support reduces service satisfaction.")
        if seniorcitizen == 1:
            reasons.append("Senior citizens show higher churn risk.")

        if reasons:
            for r in reasons:
                st.write("•", r)
        else:
            st.write("• This customer shows strong retention indicators.")

        # -------------------------------
        # 🧾 DOWNLOAD REPORT
        # -------------------------------
        report = payload.copy()
        report["churn_probability"] = round(prob, 2)
        report["risk_level"] = "High" if prob > 0.6 else "Medium" if prob > 0.4 else "Low"

        report_df = pd.DataFrame([report])

        st.download_button(
            label="🧾 Download Churn Report (CSV)",
            data=report_df.to_csv(index=False),
            file_name="churn_report.csv",
            mime="text/csv"
        )

    else:
        st.error("❌ API error. Please try again.")
