import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Load model
model = joblib.load("model/diabetes_model.pkl")
scaler = joblib.load("model/scaler.pkl")

st.set_page_config(page_title="Diabetes Prediction", layout="wide")

st.title("🩺 Diabetes Prediction System")

# Inputs
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.slider("Pregnancies", 0, 17, 3)
    glucose = st.slider("Glucose", 0, 200, 120)
    blood_pressure = st.slider("Blood Pressure", 0, 122, 72)
    skin_thickness = st.slider("Skin Thickness", 0, 99, 23)

with col2:
    insulin = st.slider("Insulin", 0, 846, 79)
    bmi = st.slider("BMI", 0.0, 67.0, 32.0)
    dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.47)
    age = st.slider("Age", 21, 100, 33)

# Predict
if st.button("Predict"):
    data = np.array([[pregnancies, glucose, blood_pressure,
                      skin_thickness, insulin, bmi, dpf, age]])
    
    scaled = scaler.transform(data)
    pred = model.predict(scaled)[0]
    prob = model.predict_proba(scaled)[0][1] * 100

    # Result
    st.subheader("📊 Result")
    st.write(f"**Status:** {'DIABETIC' if pred==1 else 'NON-DIABETIC'}")
    st.write(f"**Probability:** {prob:.2f}%")

    # Chart
    fig, ax = plt.subplots()
    ax.bar(["Risk"], [prob])
    ax.set_ylim(0, 100)
    st.pyplot(fig)

    # Feature importance
    st.subheader("🔍 Feature Importance")
    fig2, ax2 = plt.subplots()
    ax2.barh(
        ["Preg", "Glucose", "BP", "Skin", "Insulin", "BMI", "DPF", "Age"],
        model.feature_importances_
    )
    st.pyplot(fig2)