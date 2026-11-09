from django.urls import path
from . import views

urlpatterns = [
    path("", views.worklist, name="worklist"),
    path("new/", views.new_discharge, name="new"),
    path("done/<int:pk>/", views.mark_done, name="done"),
]