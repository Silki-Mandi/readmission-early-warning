import pandas as pd, numpy as np, joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.utils.class_weight import compute_sample_weight

# 1. Load and clean
raw = pd.read_csv("data/diabetic_data.csv", na_values="?")
raw = raw[~raw.discharge_disposition_id.isin([11, 13, 14, 19, 20, 21])]
raw = raw.drop_duplicates(subset="patient_nbr")

# 2. Feature engineering
df = pd.DataFrame()
df["patient_id"] = "P" + raw["patient_nbr"].astype(str)
df["days_in_hospital"] = raw["time_in_hospital"]
df["num_medications"] = raw["num_medications"]
df["age"] = raw["age"].str.extract(r"\[(\d+)")[0].astype(int) + 5
df["previous_visits"] = raw["number_outpatient"] + raw["number_emergency"] + raw["number_inpatient"]
df["readmitted_30d"] = (raw["readmitted"] == "<30").astype(int)

def group_dx(code):
    try:
        c = float(code)
    except (TypeError, ValueError):
        return "Other"
    if 250 <= c < 251: return "Diabetes"
    if 390 <= c <= 459: return "Circulatory"
    if 460 <= c <= 519: return "Respiratory"
    if 520 <= c <= 579: return "Digestive"
    if 580 <= c <= 629: return "Genitourinary"
    return "Other"

df["diagnosis_code"] = raw["diag_1"].apply(group_dx)
df.to_csv("data/patient_discharges.csv", index=False)
print("Rows:", len(df), "| readmit rate:", round(df.readmitted_30d.mean(), 3))

# 3. Split and train
num = ["age", "days_in_hospital", "num_medications", "previous_visits"]
X, y = df[num + ["diagnosis_code"]], df["readmitted_30d"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
prep = ColumnTransformer(
    [("num", "passthrough", num),
     ("cat", OneHotEncoder(sparse_output=False, handle_unknown="ignore"), ["diagnosis_code"])],
    verbose_feature_names_out=False)
pipe = Pipeline([("prep", prep),
                 ("clf", GradientBoostingClassifier(n_estimators=200, learning_rate=0.05,
                                                    max_depth=3, random_state=42))])
pipe.fit(Xtr, ytr, clf__sample_weight=compute_sample_weight("balanced", ytr))

# 4. Evaluate
proba = pipe.predict_proba(Xte)[:, 1]
print("ROC-AUC:", round(roc_auc_score(yte, proba), 3))

# 5. Save
joblib.dump(pipe, "ml/model.joblib")
joblib.dump({"high": float(np.percentile(proba, 90)),
             "medium": float(np.percentile(proba, 70))}, "ml/thresholds.joblib")
print("Saved ml/model.joblib and ml/thresholds.joblib")