from django import forms
from .models import Discharge

DX = ["Circulatory", "Respiratory", "Diabetes", "Digestive", "Genitourinary", "Other"]


class DischargeForm(forms.ModelForm):
    diagnosis_code = forms.ChoiceField(choices=[(d, d) for d in DX])

    class Meta:
        model = Discharge
        fields = ["patient_id", "age", "diagnosis_code", "days_in_hospital",
                  "num_medications", "previous_visits"]