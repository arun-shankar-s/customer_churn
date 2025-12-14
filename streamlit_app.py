import streamlit as st
import requests

API_URL = "https://customerchurn-production.up.railway.app/predict"

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📡",
    layout="wide"
)

# ---------- HEADER ----------
st.title("📡 Customer Churn Prediction App")
st.caption("Predict the probability of a customer cancelling their subscription")

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

# ---------- INPUT SECTIONS ----------
st.subheader("👤 Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:
    seniorcitizen = st.selectbox("Senior Citizen", [0, 1])
    tenure = st.number_input("Tenure (months)", 0, 72, 12)
    gender = st.selectbox("Gender", ["Male", "Female"])

with col2:
    monthlycharges = st.number_input("Monthly Charges", 0.0, 200.0, 70.5)
    totalcharges = st.number_input("Total Charges", 0.0, 10000.0, 800.0)
    partner = st.selectbox("Partner", ["Yes", "No"])

with col3:
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperlessbilling = st.selectbox("Paperless Billing", ["Yes", "No"])

st.markdown("---")
st.subheader("📶 Services & Billing")

col4, col5, col6 = st.columns(3)

with col4:
    phoneservice = st.selectbox("Phone Service", ["Yes", "No"])
    multiplelines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    internetservice = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

with col5:
    onlinesecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    onlinebackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    deviceprotection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])

with col6:
    techsupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    streamingtv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streamingmovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

paymentmethod = st.selectbox(
    "Payment Method",
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
)

st.markdown("---")

# ---------- PREDICTION ----------
if st.button("🔮 Predict Churn Probability", use_container_width=True):

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

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        prob = response.json()["churn_probability"]

        st.success(f"📊 **Predicted Churn Probability: {prob:.2f}**")

        # ---------- EXPLANATION ----------
        st.markdown("### 🧠 Why this customer may churn")

        reasons = []

        if tenure < 12:
            reasons.append("Low tenure → customers often churn early due to poor onboarding.")

        if contract == "Month-to-month":
            reasons.append("Month-to-month contract → low commitment increases churn risk.")

        if paymentmethod == "Electronic check":
            reasons.append("Electronic check payment → historically linked with higher churn.")

        if monthlycharges > 70:
            reasons.append("High monthly charges → price sensitivity risk.")

        if techsupport == "No":
            reasons.append("No tech support → unresolved issues may push customers to leave.")

        if reasons:
            for r in reasons:
                st.markdown(f"- {r}")
        else:
            st.markdown("- No strong churn risk signals detected based on input features.")

    else:
        st.error("❌ API error. Please try again.")
