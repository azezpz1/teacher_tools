# seat_arranger/models.py
from django.db import models
from django.contrib.auth.models import User


class ClassPeriod(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="class_periods"
    )
    period_number: models.PositiveIntegerField = models.PositiveIntegerField()

    def __str__(self):
        return f"Period {self.period_number} for {self.user.username}"


class Student(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    class_period: models.ForeignKey = models.ForeignKey(
        ClassPeriod, on_delete=models.CASCADE, related_name="students"
    )

    def __str__(self):
        return self.name
