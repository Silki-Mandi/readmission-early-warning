import pandas as pd
from django.core.management.base import BaseCommand
from risk.models import Discharge
from risk.scoring import score


class Command(BaseCommand):
    help = "Load 200 random patients from the CSV and score them"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("data/patient_discharges.csv").sample(200, random_state=1)
        for r in df.itertuples():
            p, t, f, tasks = score(r.age, r.diagnosis_code, r.days_in_hospital,
                                   r.num_medications, r.previous_visits)
            Discharge.objects.update_or_create(
                patient_id=r.patient_id,
                defaults=dict(
                    age=r.age,
                    diagnosis_code=r.diagnosis_code,
                    days_in_hospital=r.days_in_hospital,
                    num_medications=r.num_medications,
                    previous_visits=r.previous_visits,
                    risk_score=p,
                    risk_tier=t,
                    risk_factors=f,
                    tasks=tasks,
                ),
            )
        self.stdout.write("Loaded 200 patients")