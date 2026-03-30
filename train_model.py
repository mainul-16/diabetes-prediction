"""
train_model.py
--------------
Run this ONCE locally to train and save the model + scaler.
Usage: python train_model.py
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# ── 1. Load Data ──────────────────────────────────────────────────────────────
df = pd.read_csv("data/diabetes.csv")

# ── 2. Clean Data ─────────────────────────────────────────────────────────────
# Replace biologically impossible zero-values with NaN, then fill with median
zero_not_allowed = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
df[zero_not_allowed] = df[zero_not_allowed].replace(0, np.nan)
df.fillna(df.median(numeric_only=True), inplace=True)

# ── 3. Split ──────────────────────────────────────────────────────────────────
X = df.drop("Outcome", axis=1)
y = df["Outcome"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 4. Scale ──────────────────────────────────────────────────────────────────
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ── 5. Train ──────────────────────────────────────────────────────────────────
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)
model.fit(X_train_sc, y_train)

# ── 6. Evaluate ───────────────────────────────────────────────────────────────
preds = model.predict(X_test_sc)
acc   = accuracy_score(y_test, preds)
auc   = roc_auc_score(y_test, model.predict_proba(X_test_sc)[:, 1])

print(f"\n✅ Accuracy : {acc:.4f}")
print(f"✅ ROC-AUC  : {auc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, preds, target_names=["No Diabetes", "Diabetes"]))

# ── 7. Save Model & Scaler ────────────────────────────────────────────────────
os.makedirs("model", exist_ok=True)
joblib.dump(model,  "model/diabetes_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
print("✅ model/diabetes_model.pkl  saved")
print("✅ model/scaler.pkl          saved")
