from django.db import models


class Discharge(models.Model):
    patient_id = models.CharField(max_length=20, unique=True)
    age = models.IntegerField()
    diagnosis_code = models.CharField(max_length=20)
    days_in_hospital = models.IntegerField()
    num_medications = models.IntegerField()
    previous_visits = models.IntegerField()
    risk_score = models.FloatField(default=0)
    risk_tier = models.CharField(max_length=6, default="LOW")
    risk_factors = models.JSONField(default=list)
    tasks = models.JSONField(default=list)
    task_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["-risk_score"]

    def __str__(self):
        return self.patient_id