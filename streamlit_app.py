import streamlit as st
import requests

API_URL = "https://customerchurn-production.up.railway.app/predict"

st.title("📡 Customer Churn Prediction App")
st.write("Enter customer details below to predict churn probability.")

with st.expander("ℹ️ What do these fields mean?"):
    st.markdown("""
    **Senior Citizen**  
    Whether the customer is a senior citizen (1 = Yes, 0 = No).

    **Tenure**  
    Number of months the customer has stayed with the company.

    **Monthly Charges**  
    The amount billed to the customer every month.

    **Total Charges**  
    Overall amount the customer has paid so far.

    **Gender**  
    Customer gender information.

    **Partner**  
    Whether the customer has a partner (Yes/No).

    **Dependents**  
    Whether the customer has dependents (children, family members).

    **Phone Service**  
    Whether the customer has a phone service plan.

    **Multiple Lines**  
    Whether the customer uses multiple phone lines.

    **Internet Service**  
    Type of internet service (DSL, Fiber optic, None).

    **Online Security**  
    Whether the customer has online security addon service.

    **Online Backup**  
    Whether the customer has cloud backup service.

    **Device Protection**  
    Whether the customer has device protection plan.

    **Tech Support**  
    Whether tech support is included in their plan.

    **Streaming TV**  
    Access to TV streaming services.

    **Streaming Movies**  
    Access to movie streaming services.

    **Contract**  
    Type of contract (Month-to-month, One year, Two year).

    **Paperless Billing**  
    Whether customer uses paperless billing.

    **Payment Method**  
    Payment type such as electronic check, mailed check, automatic card/bank.
    """)


# ---- Inputs ----
seniorcitizen = st.selectbox("Senior Citizen", [0, 1])
tenure = st.number_input("Tenure (months)", 0, 72, 12)
monthlycharges = st.number_input("Monthly Charges", 0.0, 200.0, 70.5)
totalcharges = st.number_input("Total Charges", 0.0, 10000.0, 800.0)

gender = st.selectbox("Gender", ["Male", "Female"])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])
phoneservice = st.selectbox("Phone Service", ["Yes", "No"])
multiplelines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
internetservice = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
onlinesecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
onlinebackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
deviceprotection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
techsupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
streamingtv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
streamingmovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
paperlessbilling = st.selectbox("Paperless Billing", ["Yes", "No"])
paymentmethod = st.selectbox(
    "Payment Method",
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
)

# ---- Predict ----
if st.button("Predict Churn Probability"):
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
        st.success(f"📊 **Churn Probability: {prob:.2f}**")
    else:
        st.error("❌ API error. Please try again.")
