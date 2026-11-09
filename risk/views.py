from django.shortcuts import render, redirect, get_object_or_404
from .models import Discharge
from .forms import DischargeForm
from .scoring import score


def worklist(request):
    patients = Discharge.objects.filter(task_done=False)
    tier = request.GET.get("tier")
    if tier:
        patients = patients.filter(risk_tier=tier)
    return render(request, "risk/worklist.html", {"patients": patients[:100], "tier": tier})


def new_discharge(request):
    form = DischargeForm(request.POST or None)
    if form.is_valid():
        d = form.save(commit=False)
        d.risk_score, d.risk_tier, d.risk_factors, d.tasks = score(
            d.age, d.diagnosis_code, d.days_in_hospital,
            d.num_medications, d.previous_visits)
        d.save()
        return redirect("worklist")
    return render(request, "risk/new.html", {"form": form})


def mark_done(request, pk):
    if request.method == "POST":
        d = get_object_or_404(Discharge, pk=pk)
        d.task_done = True
        d.save()
    return redirect("worklist")