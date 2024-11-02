# seat_arranger/admin.py
from django.contrib import admin
from .models import ClassPeriod, Student


# Inline admin for adding students directly within ClassPeriod
class StudentInline(admin.TabularInline):
    model = Student
    extra = 1  # Number of blank rows for new students


@admin.register(ClassPeriod)
class ClassPeriodAdmin(admin.ModelAdmin):
    list_display = ("period_number", "user")
    search_fields = ("user__username", "period_number")
    inlines = [StudentInline]  # Inline editing for students within ClassPeriod


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "class_period")
    list_filter = ("class_period",)
