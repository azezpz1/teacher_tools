from django.urls import path
from . import views

app_name = "seat_arranger"

urlpatterns = [
    path("add-class-period/", views.add_class_period, name="add_class_period"),
]
