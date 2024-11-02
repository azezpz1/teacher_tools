# seat_arranger/admin.py
from django.contrib import admin
from .models import ClassPeriod, Student


# Inline admin for adding/removing students within ClassPeriod
class StudentInline(admin.TabularInline):
    model = ClassPeriod.students.through  # Intermediate model for the ManyToManyField
    extra = 1  # Number of extra blank student slots


@admin.register(ClassPeriod)
class ClassPeriodAdmin(admin.ModelAdmin):
    list_display = (
        "period_number",
        "user",
        "created_at",
    )  # Display period number, user, and created date
    search_fields = (
        "user__username",
        "period_number",
    )  # Add search fields for easier filtering
    inlines = [StudentInline]  # Inline editing for students


# Register the Student model separately
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Display student names
