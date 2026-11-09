@'
# Hospital Patient Readmission Early Warning System

Scores patients at discharge for their risk of returning to hospital within
30 days, ranks them in a nurse worklist, explains the risk factors, and
recommends follow-up tasks (for example, "Schedule telehealth call within 3 days").

Built with Django, scikit-learn (Gradient Boosting) and SQLite.

## Live demo

Live app: https://silkimandi05.pythonanywhere.com

## Dataset

Diabetes 130-US Hospitals (1999-2008), from Kaggle. Download diabetic_data.csv
and place it in the data/ folder if you want to retrain the model.

## Results

- Trained on 69,990 patients; 9% were readmitted within 30 days.
- ROC-AUC on held-out test data: 0.60.
- The score is used to rank patients so nurses can prioritise follow-up.
  A moderate AUC is typical for readmission prediction.

## Run locally