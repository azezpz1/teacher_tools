from django import forms


class ClassPeriodForm(forms.Form):
    period_number = forms.IntegerField(label="Period Number", min_value=1, max_value=8)
    student_names = forms.CharField(
        label="Student Names",
        widget=forms.Textarea(attrs={"placeholder": "Enter one name per line"}),
        help_text="Enter names, one per line",
    )
