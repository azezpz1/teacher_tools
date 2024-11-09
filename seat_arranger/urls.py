from django.urls import path
from .views import add_class_period, classroom

app_name = "seat_arranger"

urlpatterns = [
    path("add-class-period/", add_class_period, name="add_class_period"),
    path("classroom/", classroom, name="classroom"),
]
