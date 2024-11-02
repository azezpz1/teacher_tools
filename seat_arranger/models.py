from django.db import models
from django.contrib.auth.models import User


class ClassPeriod(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="class_periods"
    )
    period_number: models.PositiveIntegerField = models.PositiveIntegerField()  # 1 to 8
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Period {self.period_number}"


class Student(models.Model):
    class_period: models.ForeignKey = models.ForeignKey(
        ClassPeriod, on_delete=models.CASCADE, related_name="students"
    )
    name: models.CharField = models.CharField(max_length=100)

    def __str__(self):
        return self.name
