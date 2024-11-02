from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    name: models.CharField = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassPeriod(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="class_periods"
    )
    students: models.ManyToManyField = models.ManyToManyField(
        Student, related_name="class_periods"
    )  # Changed to ManyToMany
    period_number: models.PositiveIntegerField = models.PositiveIntegerField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Period {self.period_number}"
