import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from seat_arranger.seating import create_seating_arrangement
from .forms import ClassPeriodForm
from .models import ClassPeriod, Student, TableLayout

logger = logging.getLogger("seat_arranger")


@login_required
def add_class_period(request):
    if request.method == "POST":
        logger.info(f"Adding/updating class period for user {request.user.username}")
        form = ClassPeriodForm(request.POST)
        if form.is_valid():
            period_number = form.cleaned_data["period_number"]
            student_names = form.cleaned_data["student_names"].splitlines()
            logger.info(
                f"Processing period {period_number} with {len(student_names)} students"
            )

            class_period, created = ClassPeriod.objects.get_or_create(
                user=request.user, period_number=period_number
            )
            if created:
                logger.info(f"Created new class period {period_number}")
            else:
                logger.info(f"Updating existing class period {period_number}")

            # Clear existing students to allow updates
            class_period.students.all().delete()
            logger.info("Cleared existing students")

            # Add each name as a Student object
            student_count = 0
            for name in student_names:
                if name.strip():  # Ignore empty lines
                    Student.objects.create(class_period=class_period, name=name.strip())
                    student_count += 1
            logger.info(f"Added {student_count} students to period {period_number}")

            messages.success(
                request, f"Class Period {period_number} saved successfully!"
            )
            return redirect("seat_arranger:add_class_period")
        else:
            logger.warning(f"Invalid form submission: {form.errors}")
    else:
        form = ClassPeriodForm()
    return render(request, "seat_arranger/add_class_period.html", {"form": form})


@login_required
def classroom(request, period_number):
    logger.info(
        f"Accessing classroom view for period {period_number} by user {request.user.username}"
    )
    # First check if table layout exists
    try:
        table_layout = TableLayout.objects.get(user=request.user)
    except TableLayout.DoesNotExist:
        logger.warning(f"No table layout found for user {request.user.username}")
        messages.warning(request, "Please set up your classroom layout first")
        return redirect("seat_arranger:add_table_layout")

    # Get class period and students
    class_period = get_object_or_404(
        ClassPeriod, user=request.user, period_number=period_number
    )
    students = list(class_period.students.values_list("name", flat=True))

    # Count available seats (True values in layout)
    available_seats = sum(1 for x in table_layout.layout if x)

    # Check if we have enough seats
    if len(students) > available_seats:
        messages.error(
            request,
            f"Your classroom layout has {available_seats} seats, but you have {len(students)} students. "
            "Please update your layout to accommodate all students.",
        )
        return redirect("seat_arranger:add_table_layout")

    # Create seating arrangement using table layout
    seating = create_seating_arrangement(
        students, table_layout.width, table_layout.depth, table_layout.layout
    )

    return render(
        request,
        "seat_arranger/classroom.html",
        {"seating": seating, "period_number": period_number},
    )


@require_POST
def reshuffle_seats(request):
    logger.info(f"Reshuffling seats for user {request.user.username}")
    return JsonResponse({"success": True})


@login_required
def add_table_layout(request):
    logger.info(f"Accessing table layout view for user {request.user.username}")
    if request.method == "POST":
        width = int(request.POST.get("width"))
        depth = int(request.POST.get("depth"))
        layout = request.POST.getlist("layout[]")

        # Convert layout strings to booleans
        layout = [item == "true" for item in layout]

        # Update or create the layout
        TableLayout.objects.update_or_create(
            user=request.user,
            defaults={"width": width, "depth": depth, "layout": layout},
        )

        return JsonResponse({"status": "success"})

    # GET request - show the form
    try:
        layout = TableLayout.objects.get(user=request.user)
        initial_data = {
            "width": layout.width,
            "depth": layout.depth,
            "layout": ["true" if x else "false" for x in layout.layout],
        }
    except TableLayout.DoesNotExist:
        initial_data = {
            "width": 5,
            "depth": 5,
            "layout": ["true"] * (5 * 5),  # Default 5x5 grid, all tables present
        }

    return render(request, "seat_arranger/add_table_layout.html", initial_data)
