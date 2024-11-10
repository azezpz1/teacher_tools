from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from seat_arranger.seating import create_seating_arrangement
from .forms import ClassPeriodForm
from .models import ClassPeriod, Student


@login_required
def add_class_period(request):
    if request.method == "POST":
        form = ClassPeriodForm(request.POST)
        if form.is_valid():
            period_number = form.cleaned_data["period_number"]
            student_names = form.cleaned_data["student_names"].splitlines()

            class_period, _ = ClassPeriod.objects.get_or_create(
                user=request.user, period_number=period_number
            )

            # Clear existing students to allow updates
            class_period.students.all().delete()

            # Add each name as a Student object
            for name in student_names:
                if name.strip():  # Ignore empty lines
                    Student.objects.create(class_period=class_period, name=name.strip())

            messages.success(
                request, f"Class Period {period_number} saved successfully!"
            )
            return redirect("seat_arranger:add_class_period")
    else:
        form = ClassPeriodForm()
    return render(request, "seat_arranger/add_class_period.html", {"form": form})


@login_required
def classroom(request):
    # Example student list - in practice, you'd get this from your database
    students = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"]
    seating = create_seating_arrangement(students)
    return render(request, "seat_arranger/classroom.html", {"seating": seating})


@require_POST
def reshuffle_seats(request):
    # For now, just return success - we'll add actual reshuffling later
    return JsonResponse({"success": True})
