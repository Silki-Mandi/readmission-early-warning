import joblib, pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
model = joblib.load(BASE / "ml/model.joblib")
TH = joblib.load(BASE / "ml/thresholds.joblib")


def tier(p):
    if p >= TH["high"]:
        return "HIGH"
    if p >= TH["medium"]:
        return "MEDIUM"
    return "LOW"


def explain(age, dx, days, meds, prev):
    factors, tasks = [], []
    if meds >= 10:
        factors.append(f"{meds} medications")
        tasks.append("Pharmacist medication reconciliation; provide pill organizer and written schedule")
    if days >= 7:
        factors.append(f"Long stay ({days} days)")
        tasks.append("Schedule telehealth call within 3 days; confirm home support")
    if prev >= 3:
        factors.append(f"{prev} previous visits")
        tasks.append("Assign care coordinator; book primary-care visit within 7 days")
    if age >= 75:
        factors.append(f"Age {age}")
        tasks.append("Arrange home-health check and fall-risk review")

    dx_tasks = {
        "Circulatory": "Daily weight and BP monitoring teaching; cardiology follow-up in 7 days",
        "Respiratory": "Inhaler technique check; pulmonary follow-up in 7 days",
        "Diabetes": "Glucose log teaching; endocrine follow-up in 7 days",
        "Genitourinary": "Hydration and renal advice; follow-up in 7 days",
    }
    if dx in dx_tasks:
        factors.append(f"Diagnosis: {dx}")
        tasks.append(dx_tasks[dx])
    return factors, tasks


def score(age, diagnosis_code, days_in_hospital, num_medications, previous_visits):
    row = pd.DataFrame([dict(
        age=age,
        days_in_hospital=days_in_hospital,
        num_medications=num_medications,
        previous_visits=previous_visits,
        diagnosis_code=diagnosis_code,
    )])
    p = float(model.predict_proba(row)[0, 1])
    t = tier(p)
    factors, tasks = explain(age, diagnosis_code, days_in_hospital,
                             num_medications, previous_visits)
    if t == "HIGH":
        tasks.insert(0, "Nurse call within 48 hours")
    return p, t, factors, tasks