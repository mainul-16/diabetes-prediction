"""
app.py — Diabetes Prediction System (Improved Version)
Run: python app.py
"""

import gradio as gr
import joblib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Load model & scaler ───────────────────────────────────────────────────────
model  = joblib.load("model/diabetes_model.pkl")
scaler = joblib.load("model/scaler.pkl")

FEATURES = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

# ── Prediction function ───────────────────────────────────────────────────────
def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness,
                     insulin, bmi, dpf, age):

    input_data = np.array([[pregnancies, glucose, blood_pressure,
                            skin_thickness, insulin, bmi, dpf, age]])
    input_scaled = scaler.transform(input_data)

    prediction  = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    prob_diabetic = probability[1] * 100

    # Risk level
    if prob_diabetic < 30:
        risk  = "🟢 LOW RISK"
        color = "#2ecc71"
    elif prob_diabetic < 60:
        risk  = "🟡 MODERATE RISK"
        color = "#f39c12"
    else:
        risk  = "🔴 HIGH RISK"
        color = "#e74c3c"

    # ✅ NEW STRUCTURED OUTPUT
    result = f"""
# 🩺 Diabetes Prediction Report

## 📌 Prediction Result
➡️ **Status:** {"DIABETIC" if prediction == 1 else "NON-DIABETIC"}

## 📊 Probability Analysis
➡️ **Diabetes Probability:** {prob_diabetic:.1f}%

## ⚠️ Risk Level
➡️ {risk}

## 🧠 Interpretation
{"High likelihood of diabetes detected. Please consult a doctor." if prediction == 1 else "Low risk detected. Maintain a healthy lifestyle."}

---
"""

    # ── Probability Chart ─────────────────────────────────────────────────────
    fig1, ax1 = plt.subplots(figsize=(5, 2))
    ax1.barh(["Risk"], [prob_diabetic], color=color, height=0.4)
    ax1.barh(["Risk"], [100 - prob_diabetic], left=[prob_diabetic],
             color="#ecf0f1", height=0.4)
    ax1.set_xlim(0, 100)
    ax1.set_xlabel("Probability (%)")
    ax1.set_title(f"Diabetes Probability: {prob_diabetic:.1f}%",
                  fontweight="bold", color=color)
    ax1.axvline(x=50, color="#aaa", linestyle="--", linewidth=1)
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.tick_params(left=False)
    plt.tight_layout()

    # ── Feature Importance Chart ──────────────────────────────────────────────
    importances = model.feature_importances_
    sorted_idx  = np.argsort(importances)

    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.barh([FEATURES[i] for i in sorted_idx],
             importances[sorted_idx], color="#3498db")
    ax2.set_xlabel("Importance Score")
    ax2.set_title("Feature Importance", fontweight="bold")
    ax2.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    return result, fig1, fig2


# ── Save report function ──────────────────────────────────────────────────────
def save_report(result):
    with open("report.txt", "w") as f:
        f.write(result)
    return "report.txt"


# ── Build UI ──────────────────────────────────────────────────────────────────
with gr.Blocks(title="Diabetes Prediction System") as demo:

    gr.Markdown("# 🩺 Diabetes Prediction System\nEnter patient data and click **Predict**.")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📋 Patient Data")

            pregnancies    = gr.Slider(0, 17, value=3, step=1, label="Pregnancies")
            glucose        = gr.Slider(0, 200, value=120, step=1, label="Glucose (mg/dL)")
            blood_pressure = gr.Slider(0, 122, value=72, step=1, label="Blood Pressure (mm Hg)")
            skin_thickness = gr.Slider(0, 99, value=23, step=1, label="Skin Thickness (mm)")
            insulin        = gr.Slider(0, 846, value=79, step=1, label="Insulin (mu U/ml)")
            bmi            = gr.Slider(0, 67, value=32.0, step=0.1, label="BMI (kg/m2)")
            dpf            = gr.Slider(0, 2.5, value=0.47, step=0.01, label="Diabetes Pedigree Function")
            age            = gr.Slider(21, 100, value=33, step=1, label="Age (years)")

            predict_btn = gr.Button("Predict", variant="primary")
            download_btn = gr.Button("Download Report")

        with gr.Column():
            gr.Markdown("## 📊 Prediction Output")

            result_text = gr.Markdown()

            gr.Markdown("### 📈 Probability Chart")
            prob_chart = gr.Plot()

            gr.Markdown("### 🔍 Feature Importance")
            import_chart = gr.Plot()

            file_output = gr.File()

    # Example inputs
    gr.Examples(
        examples=[
            [6, 148, 72, 35, 0, 33.6, 0.627, 50],
            [1, 85, 66, 29, 0, 26.6, 0.351, 31],
            [8, 183, 64, 0, 0, 23.3, 0.672, 32],
            [1, 89, 66, 23, 94, 28.1, 0.167, 21],
        ],
        inputs=[pregnancies, glucose, blood_pressure, skin_thickness,
                insulin, bmi, dpf, age],
    )

    gr.Markdown("> ⚕️ For educational purposes only. Not a substitute for medical advice.")

    # Button actions
    predict_btn.click(
        fn=predict_diabetes,
        inputs=[pregnancies, glucose, blood_pressure, skin_thickness,
                insulin, bmi, dpf, age],
        outputs=[result_text, prob_chart, import_chart]
    )

    download_btn.click(
        fn=save_report,
        inputs=result_text,
        outputs=file_output
    )


# ── Run app ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(share=True)