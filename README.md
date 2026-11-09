# Hospital Patient Readmission Early Warning System

Scores patients at discharge for their risk of returning to hospital within
30 days, ranks them in a nurse worklist, explains the risk factors, and
recommends follow-up tasks (for example, "Schedule telehealth call within 3 days").

Built with Django, scikit-learn (Gradient Boosting) and SQLite.

## Dataset
Diabetes 130-US Hospitals (1999-2008), from Kaggle. Download `diabetic_data.csv`
and place it in the `data/` folder if you want to retrain the model.

## Run locally
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python ml/train.py
python manage.py migrate
python manage.py load_discharges
python manage.py runserver
```
Then open http://127.0.0.1:8000

## Live demo
Link: https://silkimandi05.pythonanywhere.com

## Results
- Trained on 69,990 patients; 9% were readmitted within 30 days.
- ROC-AUC on held-out test data: 0.60.
- The score is used to rank patients so nurses can prioritise follow-up. A moderate AUC is typical for readmission prediction.

## Limitations
- Trained on diabetic inpatients only, with data from 1999 to 2008.
- Moderate accuracy, which is typical for readmission prediction.
- Decision support for nurses, not a diagnostic tool.