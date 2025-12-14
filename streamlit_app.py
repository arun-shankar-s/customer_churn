import streamlit as st
import requests

API_URL = "https://customerchurn-production.up.railway.app/predict"

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📡",
    layout="wide"
)

# ---------- HEADER ----------
st.title("📡 Customer Churn Prediction")
st.caption("Predict the probability of a customer leaving based on behavior and subscription details.")

st.markdown("---")

# ---------- INFO EXPANDER ----------
with st.expander("ℹ️ What do these fields mean?"):
    st.markdown("""
**Senior Citizen** – Customer is aged 60+  
**Tenure** – Months the customer has stayed with the company  
**Monthly Charges** – Monthly billing amount  
**Total Charges** – Lifetime amount paid  

**Partner** – Whether the customer has a spouse/partner  
**Dependents** – Children or family members dependent on the customer  

**Phone / Internet Services** – Type of services subscribed  
**Online Security / Backup / Tech Support** – Add-on protection services  

**Contract** – Subscription commitment duration  
**Paperless Billing** – Digital billing preference  
**Payment Method** – How the customer pays their bills  
""")

# ---------- CUSTOMER PROFILE ----------
st.subheader("👤 Customer Profile")
col1, col2 = st.columns(2)

with col1:
    seniorcitizen = st.selectbox("Senior Citizen", [0, 1])
    gender = st.selectbox("Gender", ["Male", "Female"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])

with col2:
    tenure = st.number_input("Tenure (months)", 0, 72, 12)
    monthlycharges = st.number_input("Monthly Charges", 0.0, 200.0, 70.5)
    totalcharges = st.number_input("Total Charges", 0.0, 10000.0, 800.0)

# ---------- SERVICES ----------
st.subheader("📶 Services")
col3, col4 = st.columns(2)

with col3:
    phoneservice = st.selectbox("Phone Service", ["Yes", "No"])
    multiplelines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    internetservice = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    streamingtv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streamingmovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

with col4:
    onlinesecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    onlinebackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    deviceprotection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    techsupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])

# ---------- BILLING ----------
st.subheader("💳 Billing Details")
col5, col6 = st.columns(2)

with col5:
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperlessbilling = st.selectbox("Paperless Billing", ["Yes", "No"])

with col6:
    paymentmethod = st.selectbox(
        "Payment Method",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    )

st.markdown("---")

# ---------- PREDICTION ----------
if st.button("🔍 Predict Churn Probability", use_container_width=True):

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
        "onlinebackup": onlinebackup,
        "deviceprotection": deviceprotection,
        "techsupport": techsupport,
        "streamingtv": streamingtv,
        "streamingmovies": streamingmovies,
        "contract": contract,
        "paperlessbilling": paperlessbilling,
        "paymentmethod": paymentmethod
    }

    with st.spinner("Analyzing customer risk..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        prob = response.json()["churn_probability"]

        if prob >= 0.7:
            st.error(f"🚨 High Churn Risk: **{prob:.2f}**")
        elif prob >= 0.4:
            st.warning(f"⚠️ Medium Churn Risk: **{prob:.2f}**")
        else:
            st.success(f"✅ Low Churn Risk: **{prob:.2f}**")

    else:
        st.error("❌ API error. Please try again.")
