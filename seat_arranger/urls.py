from django.urls import path
from .views import add_class_period, classroom, reshuffle_seats

app_name = "seat_arranger"

urlpatterns = [
    path("add-class-period/", add_class_period, name="add_class_period"),
    path("reshuffle/", reshuffle_seats, name="reshuffle_seats"),
    path('classroom/<int:period_number>/', classroom, name='classroom'),
]
